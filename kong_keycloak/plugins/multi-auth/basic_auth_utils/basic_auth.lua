local crypto = require "kong.plugins.multi-auth.basic_auth_utils.crypto"


local decode_base64 = ngx.decode_base64
local re_gmatch = ngx.re.gmatch
local re_match = ngx.re.match
local re_gsub = ngx.re.gsub
local kong = kong
-- Fast lookup for credential retrieval depending on the type of the authentication
--
-- All methods must respect:
--
-- @param request ngx request object
-- @param {table} conf Plugin config
-- @return {string} public_key
-- @return {string} private_key
local function retrieve_credentials(conf)
  local username, password
  local authorization_header = kong.request.get_header("authorization")

  if authorization_header then
    local iterator, iter_err = re_gmatch(authorization_header, "\\s*[Bb]asic\\s*(.+)", "oj")
    if not iterator then
      kong.log.err(iter_err)
      return
    end

    local m, err = iterator()
    if err then
      kong.log.err(err)
      return
    end

    if m and m[1] then
      local decoded_basic = decode_base64(m[1])
      if decoded_basic then
        local basic_parts, err = re_match(decoded_basic, "([^:]+):(.*)", "oj")
        if err then
          kong.log.err(err)
          return
        end

        if not basic_parts then
          kong.log.err("header has unrecognized format")
          return
        end

        username = basic_parts[1]
        password = basic_parts[2]        
      end
    end
  end

  if conf.hide_credentials then
    kong.service.request.clear_header("authorization")
  end

  return username, password
end

local function extract_jwt_from_response(res)
  if res then
    local trimmed_response = re_gsub(res,[[\s*\:\s*]],":")
    local iterator, iter_err = re_gmatch(trimmed_response, [[(?<=access_token[\W+].\")(.*?)(?=\",)]])
    if not iterator then
        return nil, iter_err
    end

    local m, err = iterator()
    if err then
        return nil, err
    end

    if m and #m > 0 then
        return m[1]
    end
  end
end

local function new_auth_request(conf)
  local given_username, given_password = retrieve_credentials(conf)
  local httpc = require("resty.http").new()
  local uri = string.format("http://%s:%s/realms/%s/protocol/openid-connect/token",conf.keycloak_host,conf.keycloak_port,conf.keycloak_realm)
  local res, err = httpc:request_uri(uri, {
      method = "POST",
      body = string.format("client_id=%s&grant_type=password&username=%s&password=%s",conf.keycloak_client_id,given_username,given_password),
      headers = {
          ["Content-Type"] = "application/x-www-form-urlencoded",
      },
  })
  if not res or res.status ~= 200 then
    ngx.log(ngx.ERR, "request failed: ", err)
    return
  end
  local jwt = extract_jwt_from_response(res.body)
  ngx.req.set_header("authorization",string.format("Bearer %s",jwt))
end


local function basic_auth_login(conf)
  if conf.anonymous and kong.client.get_credential() then
    -- we're already authenticated, and we're configured for using anonymous,
    -- hence we're in a logical OR between auth methods and we're already done.
    return
  end
  -- 2. make up jwt body request
  ---3. create request, 
  new_auth_request(conf)
  
end


return {
    basic_auth_login = basic_auth_login
}