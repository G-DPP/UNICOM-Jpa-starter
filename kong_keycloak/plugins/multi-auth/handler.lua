local access = require "kong.plugins.multi-auth.access"
local priority_env_var = "JWT_KEYCLOAK_PRIORITY"
local priority
if os.getenv(priority_env_var) then
    priority = tonumber(os.getenv(priority_env_var))
else
    priority = 1005
end
kong.log.debug('JWT_KEYCLOAK_PRIORITY: ' .. priority)

local MultiAuthHandler = {
  VERSION  = "0.0.1",
  PRIORITY = priority,
}

function MultiAuthHandler:access(conf)
    access.execute(conf)
end

return MultiAuthHandler




