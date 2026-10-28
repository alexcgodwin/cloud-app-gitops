"""Validate rendered Kustomize resource contracts, not live cluster health."""
import json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ENVIRONMENTS={'dev':'devops-preview','staging':'devops-staging','prod':'devops-prod'}

def check_rendered_yaml(yaml_documents, environment):
    expected_namespace=ENVIRONMENTS[environment]
    docs=[x for x in yaml_documents if x]
    bykind={}
    for d in docs:
        kind=d.get('kind');bykind.setdefault(kind,[]).append(d)
        if kind!='Namespace' and d.get('metadata',{}).get('namespace')!=expected_namespace:
            raise AssertionError(f'{kind}: incorrect namespace')
    for kind in ('Namespace','Deployment','Service','HorizontalPodAutoscaler','PodDisruptionBudget','NetworkPolicy'):
        if len(bykind.get(kind,[]))!=1:raise AssertionError(f'{kind}: expected exactly one')
    deploy=bykind['Deployment'][0]
    pod=deploy['spec']['template']['spec']
    assert pod['securityContext']['runAsNonRoot'] is True
    container=pod['containers'][0]
    assert container['securityContext']['allowPrivilegeEscalation'] is False
    assert container['securityContext']['readOnlyRootFilesystem'] is True
    assert 'ALL' in container['securityContext']['capabilities']['drop']
    assert container['resources']['requests']['cpu']
    assert container['readinessProbe']['httpGet']['path']=='/health'
    assert 'startupProbe' in container
    assert bykind['Namespace'][0]['metadata']['name']==expected_namespace
    hpa=bykind['HorizontalPodAutoscaler'][0]['spec']
    assert hpa['maxReplicas']>=hpa['minReplicas']>=1
    assert bykind['PodDisruptionBudget'][0]['spec']['minAvailable']<=hpa['minReplicas']
    return {"namespace":expected_namespace,"resources":len(docs),"replicas":hpa['minReplicas']}

def validate():
    import yaml
    results=[]
    for env in ENVIRONMENTS:
        proc=subprocess.run(['kubectl','kustomize',str(ROOT/'releases'/'overlays'/env)],capture_output=True,text=True)
        if proc.returncode:raise AssertionError(f'kubectl kustomize {env}: {proc.stderr}')
        result=check_rendered_yaml(list(yaml.safe_load_all(proc.stdout)),env)
        results.append(result)
    print(json.dumps(results,indent=2))

if __name__=='__main__':validate()
