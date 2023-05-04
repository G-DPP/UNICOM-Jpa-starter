local kong = kong
local basic_auth_login = require("kong.plugins.multi-auth.basic_auth_utils.basic_auth").basic_auth_login
local keycloak_authenticate = require("kong.plugins.multi-auth.keycloak_jwt_utils.jwt_auth").keycloak_authenticate
local _M = {}
local realm = 'Basic realm="' .. _KONG._NAME .. '"'


function _M.execute(conf)
    
    if not (kong.request.get_header("authorization") or kong.request.get_header("proxy-authorization")) then        
        return kong.response.error(401, "Unauthorized", {["WWW-Authenticate"] = realm})
    end

    if string.find(kong.request.get_header("authorization"),"Basic") then
        basic_auth_login(conf)
    end
    
    keycloak_authenticate(conf)
        
end
   
return _M

