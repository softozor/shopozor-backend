import com.hivext.api.core.utils.Transport
import org.yaml.snakeyaml.Yaml

function checkJelasticResponse(response, errorMsg) {
  if (!response || response.result !== 0) {
    throw errorMsg + ': ' + response
  }
}

function addContainerEnvVars(envVars) {
  const resp = jelastic.environment.control.AddContainerEnvVars(
    '${env.envName}',
    session,
    'cp',
    envVars
  )
  checkJelasticResponse(
    resp,
    'Adding container env vars on node group <' + 'cp' + '> failed!'
  )
  return resp.object
}

function setJwtEnvVars(url) {
  var envVars = new Yaml().load(new Transport().get(url))
  addContainerEnvVars(envVars)
  const SUCCESS_RESPONSE = { result: 0 }
  return SUCCESS_RESPONSE
}

return setJwtEnvVars(
  getParam('url')
)
