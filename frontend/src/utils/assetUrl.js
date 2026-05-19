import api from "../api/axios";

export function resolveBackendAssetUrl(url) {
  if (!url) return "";
  if (/^(https?:|blob:|data:|mailto:)/i.test(url)) return url;

  const apiBase = api.defaults.baseURL || "";
  const backendOrigin = apiBase.replace(/\/api\/v1\/?$/, "");

  if (url.startsWith("/")) {
    return `${backendOrigin}${url}`;
  }

  return url;
}
