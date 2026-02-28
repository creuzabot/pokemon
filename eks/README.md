# Creuza no EKS

## Pré-requisitos
- Cluster EKS `creuza-cluster` rodando em `us-east-1`
- DynamoDB `creuza-state` criado
- ECR criado
- AWS Load Balancer Controller instalado no cluster

## Deploy

### 1. Build e push da imagem
```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws ecr create-repository --repository-name creuza --region us-east-1

aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker build -t creuza .

docker tag creuza:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/creuza:latest

docker push \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/creuza:latest
```

### 2. Substituir variáveis
```bash
# Substituir <AWS_ACCOUNT_ID> nos arquivos
sed -i "s/<AWS_ACCOUNT_ID>/$AWS_ACCOUNT_ID/g" deployment.yaml serviceaccount.yaml
```

### 3. Criar IAM Role para o ServiceAccount (IRSA)
```bash
eksctl create iamserviceaccount \
  --cluster creuza-cluster \
  --namespace creuza \
  --name creuza-sa \
  --attach-policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/creuza-dynamodb-policy \
  --approve
```

### 4. Aplicar manifests
```bash
kubectl apply -f namespace.yaml
kubectl apply -f secret.yaml
kubectl apply -f serviceaccount.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
```

### 5. Verificar
```bash
kubectl get pods -n creuza
kubectl get ingress -n creuza
```

## Notas
- Substitua `SUBSTITUA_AQUI` no `secret.yaml` pela chave Anthropic
- Substitua `SUBSTITUA_PELO_ACM_ARN` no `ingress.yaml` pelo ARN do certificado SSL
- Substitua `creuza.seudominio.com` pelo seu domínio real
- Use AWS Secrets Manager em produção em vez de secrets k8s
