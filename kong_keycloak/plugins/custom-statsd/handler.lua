local log = require "kong.plugins.custom-statsd.log"
local kong_meta = require "kong.meta"


local CustomStatsdHandler = {
  PRIORITY = 11,
  VERSION = kong_meta.version,
}


function CustomStatsdHandler:log(conf)
  log.execute(conf)
end


return CustomStatsdHandler
