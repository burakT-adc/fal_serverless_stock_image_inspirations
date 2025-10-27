# FAL.ai Serverless Deployment for Stock Image Inspirations

This folder contains the necessary files to deploy your Stock Image Inspirations generator on the [FAL.ai Serverless](https://docs.fal.ai/serverless) platform.

## 🎯 What is Stock Image Inspirations?

This serverless function generates creative, customized inspiration prompts for stock image generation. It analyzes user requirements and generates detailed, optimized prompts that can be used with AI image generation models.

## 🎯 Why FAL Serverless?

### Advantages

1. **⚡ Instant Scaling**: Instantly scales from 0 to 1000+ instances
2. **💰 Cost Optimization**: Pay only for the compute you use
3. **🚀 High Availability**: High availability with auto-scaling
4. **📊 Full Observability**: Request/response/latency monitoring
5. **🔧 Customization**: You can control your own logic
6. **🌐 Global Infrastructure**: Fast response times globally

## 📦 Installation

### 1. FAL CLI Installation

```bash
pip install fal-client[cli]
```

### 2. Authentication

```bash
fal auth login
```

This command will open a browser and ask you to log in to FAL.ai.

### 3. Setting up Secrets

Save the environment variables to be used in FAL serverless as secrets:

```bash
# OpenAI API Key (for inspiration generation)
fal secrets set OPENAI_API_KEY="sk-..."
```

## 🚀 Deployment

### Automatic Deployment

```bash
cd /Users/burak/Desktop/repos/fal_serverless_stock_image_inspirations
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment

```bash
cd /Users/burak/Desktop/repos/fal_serverless_stock_image_inspirations
fal deploy stock_inspirations_app.py
```

After deployment is complete, you will get your endpoint URL:
```
fal-ai/<your-username>/stock-image-inspirations
```

## 🔧 Integration with Your Existing Code

### Client Usage Example

```python
from stock_inspirations_fal_client import StockImageInspirationsFalServerless

# Initialize client
client = StockImageInspirationsFalServerless(
    endpoint="fal-ai/your-username/stock-image-inspirations"
)

# Generate inspirations
result = await client.generate_inspirations(
    user_prompt="lifestyle photography for a tech startup",
    style_preferences=["modern", "minimalist", "professional"],
    num_inspirations=5,
    include_keywords=True
)

print(result["inspirations"])
```

### Environment Variables

**Add to your docker-compose.yml or .env file:**

```yaml
environment:
  # To use FAL Serverless
  - FAL_SERVERLESS_INSPIRATIONS_ENDPOINT=fal-ai/your-username/stock-image-inspirations
  
  # API Keys (also required on FAL serverless side)
  - OPENAI_API_KEY=sk-...
  - FAL_API_KEY=your-fal-key
```

## 📊 Monitoring & Management

### List Deployments

```bash
fal apps list
```

### View Logs

```bash
fal logs <app-id>
```

### Performance Metrics

You can monitor the following metrics from the FAL dashboard:
- Request latency
- Success/error rates
- Cost per request

## 🎛️ Configuration Options

### Machine Types

For this CPU-based application (no GPU needed):
- `XS` - Minimal resources (0.25 vCPU, 0.5 GB RAM)
- `S` - Small (0.5 vCPU, 1 GB RAM)
- `M` - Medium (1 vCPU, 2 GB RAM) **[Recommended]**
- `L` - Large (2 vCPU, 4 GB RAM)

**Keep Alive:**
- `0`: Cold start on every request (cheap but slow)
- `300` (5 min): Moderate warm time
- `3600` (1 hour): Always ready (expensive but fast)

**Max Concurrency:**
- Maximum number of requests that can be processed simultaneously
- Automatically increased with auto-scaling

## 🧪 Testing

### Local Test

```bash
cd /Users/burak/Desktop/repos/fal_serverless_stock_image_inspirations
python test_local.py
```

### Remote Test (After deployment)

```python
import fal_client

# Call endpoint
result = fal_client.subscribe(
    "fal-ai/your-username/stock-image-inspirations",
    arguments={
        "user_prompt": "business meeting in a modern office",
        "style_preferences": ["corporate", "professional", "bright"],
        "num_inspirations": 3,
        "include_keywords": True,
        "include_negative_prompts": True
    },
    with_logs=True,
)

print(f"Generated inspirations: {len(result['inspirations'])}")
for i, inspiration in enumerate(result['inspirations'], 1):
    print(f"\n{i}. {inspiration['title']}")
    print(f"   Prompt: {inspiration['prompt']}")
    print(f"   Keywords: {', '.join(inspiration['keywords'])}")
```

## 💰 Cost Estimation

FAL Serverless pricing for CPU instances (approximate):
- **M (Medium)**: ~$0.0001/sec
- **Keep alive cost**: Machine cost × keep_alive_duration

**Example Calculation:**
- Average processing time: 2 seconds
- Machine: M (Medium)
- Keep alive: 300 seconds (5 minutes)
- Request frequency: 10 requests/minute

**Cost:**
- Per request: 2 × $0.0001 = $0.0002
- **Total: ~$0.0002/request**

**Comparison:**
- Dedicated server: ~$50/month = ~$1.67/day
- FAL Serverless (1000 requests/day): ~$0.20/day

💡 **90% cost savings!**

## 🔄 Migration Checklist

- [ ] FAL CLI installation
- [ ] FAL auth login
- [ ] Set up secrets (OPENAI_API_KEY)
- [ ] Deploy `stock_inspirations_app.py`
- [ ] Get endpoint URL
- [ ] Set `FAL_SERVERLESS_INSPIRATIONS_ENDPOINT` env variable
- [ ] Send test request
- [ ] Move to production
- [ ] Set up monitoring
- [ ] Activate cost tracking

## 🐛 Troubleshooting

### "fal auth" error
```bash
# Re-authenticate
fal auth logout
fal auth auth login
```

### "Secret not found" error
```bash
# Check secrets
fal secrets list

# Set again
fal secrets set OPENAI_API_KEY="your-key"
```

### Cold start too slow
```python
# Increase keep_alive in stock_inspirations_app.py
@fal.endpoint("/")
def generate_inspirations(...):
    ...
```

### Memory error
```python
# Use larger machine type
machine_type = "L"  # or even "XL"
```

## 📚 Additional Resources

- [FAL Serverless Documentation](https://docs.fal.ai/serverless)
- [FAL Python SDK Reference](https://docs.fal.ai/serverless/python-sdk)
- [FAL Pricing](https://fal.ai/pricing)
- [FAL Community Discord](https://discord.gg/fal)

## 🤝 Support

For your questions:
1. Join the FAL Discord community
2. Send an email to [email protected]
3. [Apply for Enterprise features](mailto:[email protected])

