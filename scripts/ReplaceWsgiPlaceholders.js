function checkJelasticResponse(response, errorMsg) {
  if (!response || response.result !== 0) {
    throw errorMsg + ': ' + response
  }
}

function getNodesInfo(envName) {
  const resp = jelastic.environment.control.GetEnvInfo(envName, session)
  checkJelasticResponse(
    resp,
    'Cannot get environment info of environment <' +
    envName +
    '>, session <' +
    session +
    '>'
  )
  return resp.nodes
}

function getListOfLoadBalancerNodeIPs() {
  var result = []
  const nodes = getNodesInfo(getParam('TARGET_APPID'))
  for (var i = 0; i < nodes.length; ++i) {
    var node = nodes[i]
    if (node.nodeType == 'nginx-dockerized') {
      result.push(node.intIP)
    }
  }
  return result
}

function replaceInBody(path, pattern, replacement) {
  const APPID = getParam('TARGET_APPID')
  const resp = jelastic.environment.file.ReplaceInBody(
    APPID,
    session,
    path,
    pattern,
    replacement,
    '', // nth
    '', // nodeType
    'cp'
  )
  checkJelasticResponse(
    resp,
    'Replacing pattern <' +
    pattern +
    '> with <' +
    replacement +
    '> in file <' +
    path +
    '> failed!'
  )
}

function getContainerEnvVars(nodeId) {
  const resp = jelastic.environment.control.GetContainerEnvVars(
    '${env.envName}',
    session,
    nodeId
  )
  checkJelasticResponse(
    resp,
    'Getting container env vars by nodeId <' + nodeId + '> failed!'
  )
  return resp.object
}

function getEnvVarValue(nodeId, key) {
  const resp = getContainerEnvVars(nodeId)
  return resp[key]
}

function replaceWsgiPlaceholders(nodeId, pathToFile, domainNames) {
  replaceInBody(
    pathToFile,
    'PATH_TO_VIRTUAL_ENV_PLACEHOLDER',
    getEnvVarValue(nodeId, 'PATH_TO_VIRTUAL_ENV')
  )
  replaceInBody(
    pathToFile,
    'SECRET_KEY_PLACEHOLDER',
    getEnvVarValue(nodeId, 'SECRET_KEY')
  )
  replaceInBody(
    pathToFile,
    'ALLOWED_HOSTS_PLACEHOLDER',
    domainNames
      .split(',')
      .concat(getListOfLoadBalancerNodeIPs())
      .toString()
  )
  replaceInBody(
    pathToFile,
    'DATABASE_URL_PLACEHOLDER',
    getEnvVarValue(nodeId, 'DATABASE_URL')
  )
  replaceInBody(
    pathToFile,
    'CACHE_URL_PLACEHOLDER',
    getEnvVarValue(nodeId, 'CACHE_URL')
  )
  replaceInBody(
    pathToFile,
    'JWT_EXPIRATION_DELTA_IN_DAYS_PLACEHOLDER',
    getEnvVarValue(nodeId, 'JWT_EXPIRATION_DELTA_IN_DAYS')
  )
  replaceInBody(
    pathToFile,
    'JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS_PLACEHOLDER',
    getEnvVarValue(nodeId, 'JWT_REFRESH_EXPIRATION_DELTA_IN_DAYS')
  )
  replaceInBody(
    pathToFile,
    'JWT_SECRET_KEY_PLACEHOLDER',
    getEnvVarValue(nodeId, 'JWT_SECRET_KEY')
  )
  replaceInBody(
    pathToFile,
    'JWT_ALGORITHM_PLACEHOLDER',
    getEnvVarValue(nodeId, 'JWT_ALGORITHM')
  )
  replaceInBody(
    pathToFile,
    'DJANGO_SETTINGS_MODULE_PLACEHOLDER',
    getEnvVarValue(nodeId, 'DJANGO_SETTINGS_MODULE')
  )
  const SUCCESS_RESPONSE = { result: 0 }
  return SUCCESS_RESPONSE
}

return replaceWsgiPlaceholders(
  getParam('nodeId'),
  getParam('pathToFile'),
  getParam('domainNames')
)
