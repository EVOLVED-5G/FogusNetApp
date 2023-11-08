(function(window) {
  window["env"] = window["env"] || {};
  // Environment variables
  //@ts-ignore
  window["env"]["backend"] = "${BACKEND_ADDRESS}";
  //@ts-ignore
  window["env"]["frontend"] = "${FRONTEND_ADDRESS}";
})(this);
