/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: "http://localhost:5000", // the running FLASK api server url
  auth0: {
    url: "dev-2bdk36rt.us", // the auth0 domain prefix
    audience: "http://localhost:5000", // the audience set for the auth0 app
    clientId: "wCs9rG4W0yGlA3OTC7esF2BDbig8xddo", // the client id generated for the auth0 app
    callbackURL: "http://localhost:4200", // the base url of the running ionic application.
  },
};
