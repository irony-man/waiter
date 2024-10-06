function getCsrfToken() {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    let cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === "csrftoken=") {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
}

class BaseHttpError extends Error {
  constructor(message, data, statusCode) {
    super(message);
    this.data = data;
    this.statusCode = statusCode;
    this.name = this.constructor.name;
    this.message = message;
    if (typeof Error.captureStackTrace === "function") {
      Error.captureStackTrace(this, this.constructor);
    } else {
      this.stack = new Error(message).stack;
    }
  }
}

export class HttpBadRequestError extends BaseHttpError {}

export class HttpNotOkError extends BaseHttpError {}

export class HttpNotFound extends BaseHttpError {}

export class HttpServerError extends BaseHttpError {}


async function execute(url, options) {
  let data;
  let response;
  const msg = "Error in processing request. Try later or contact support";

  try {
    response = await fetch(url, options);
    if (options.method !== "delete" && response.status !== 204) {
      const content = response.headers.get("Content-Type");
      if (content === "application/json") {
        data = await response.json();
      } else {
        data = response.text();
      }
    }
  } catch (e) {
    alert(msg);
  }

  if (response) {
    if (response.status === 400) {
      throw new HttpBadRequestError("Http 400 [BadRequest]", data, response.status);
    } else if (response.status === 404) {
      throw new HttpNotFound("Http 404 [Not found]", data, response.status);
    } else if (response.status > 400 && response.status < 500) {
      throw new HttpNotOkError(
        `Http ${response.status}` + ` [${response.statusText}]`,
        data, response.status
      );
    } else if (response?.status >= 500) {
      throw new HttpServerError(
        'Server Error.'
      );
    }
    return data;
  }
}

const formDataRequest = async (method, url, formData = null) => {
  const options = {
    method: method,
    redirect: 'manual',
    mode: 'same-origin',
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
      "X-CSRFToken": getCsrfToken(window.location.href),
    },
  };

  const isFormData = formData instanceof FormData;
  if (isFormData) {
    options.body = formData;
  } else {
    // JSON request
    options.body = JSON.stringify(formData);
    options.headers["Content-Type"] = "application/json";
  }

  return await execute(url, options);
};

export const postRequest = async (url, formData = null) => {
  return await formDataRequest("POST", url, formData);
};

export const patchRequest = async (url, formData = null) => {
  return await formDataRequest("PATCH", url, formData);
};

export const deleteRequest = async (url) => {
  return await formDataRequest("DELETE", url, null);
};

export const getRequest = async (url, queryParams = null) => {
  const options = {
    method: "GET",
    mode: 'cors',
    redirect: 'manual',
    credentials: "same-origin",
    headers: {
      Accept: "application/json",
    },
  };

  let reqUrl = url;
  let paramsObj = queryParams;

  if (queryParams) {
    const isSearchParam = queryParams instanceof URLSearchParams;
    if (!isSearchParam) {
      paramsObj = new URLSearchParams();
      Object.keys(queryParams).forEach((key) => {
        paramsObj.append(key, queryParams[key]);
      });
    }
    reqUrl = `${url}?${paramsObj.toString()}`;
  }

  return await execute(reqUrl, options);
};

export const getRESTParams = (reqData, url) => {
  let uid = reqData instanceof FormData ? reqData.get("uid") : reqData["uid"];
  if (uid) {
    return [patchRequest, `${url}${uid}/`];
  }
  return [postRequest, url];
};

export const getUrl = (path) => {
  return `/api/v1/${path}/`;
};
