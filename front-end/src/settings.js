let DEBUG = false;
let HOST_URL = "http://64.225.29.104";
let SOCKET_URL = "ws://64.225.29.104";

if (DEBUG) {
  HOST_URL = "http://127.0.0.1:8000";
  SOCKET_URL = "ws://127.0.0.1:8000";
}

export { HOST_URL, SOCKET_URL };
