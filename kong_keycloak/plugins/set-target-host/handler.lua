local access = require "kong.plugins.set-target-host.access"

local SetTargetHostHandler = {
  PRIORITY = 805,
  VERSION = "1.0.0",
}

function SetTargetHostHandler:access(conf)
  access.execute(conf)
end

return SetTargetHostHandler
