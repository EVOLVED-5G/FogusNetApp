(function(window) {
  window["env"] = window["env"] || {};
  // Environment variables
  //@ts-ignore
  window["env"]["backend"] = "${CALLBACK_ADDRESS}:${CALLBACK_PORT}";
})(this);
