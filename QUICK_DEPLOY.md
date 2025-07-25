# Quick Kubernetes Deployment

## What You Need

1. **Kubernetes cluster** (any cloud provider or local)
2. **Domain** `grabler.me` pointed to your cluster
3. **GitHub repository** with actions enabled

## Super Quick Setup

### 1. Setup Your Cluster

```bash
./scripts/simple-setup.sh
```

**Important:** Edit the email in the ClusterIssuer that gets created!

### 2. Setup GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:

- `KUBECONFIG` - Your kubeconfig file as base64: `cat ~/.kube/config | base64 -w 0`
- `POSTGRES_PASSWORD` - A secure password for PostgreSQL
- `SECRET_KEY` - A secret key for JWT (32+ characters)

### 3. Point Your Domain

Point both `grabler.me` and `api.grabler.me` to your cluster's external IP:

```bash
# Get your cluster's external IP
kubectl get services -n ingress-nginx
```

### 4. Deploy

Just push to main branch:

```bash
git add .
git commit -m "Deploy to Kubernetes"
git push origin main
```

That's it! Your app will be available at:

- Frontend: https://grabler.me
- API: https://api.grabler.me/docs

## Check Status

```bash
kubectl get pods -n namo
kubectl get ingress -n namo
```

## If Something Goes Wrong

```bash
# Check what's happening
kubectl get pods -n namo
kubectl describe pod [pod-name] -n namo
kubectl logs [pod-name] -n namo

# Check SSL certificate
kubectl get certificates -n namo
kubectl describe certificate namo-tls-secret -n namo
```

## What Gets Deployed

- ✅ PostgreSQL with persistent storage (your data survives restarts)
- ✅ FastAPI backend (2 replicas)
- ✅ Vue.js frontend (2 replicas)
- ✅ HTTPS with automatic SSL certificates
- ✅ Automatic deployment on git push

That's all you need to get started!
