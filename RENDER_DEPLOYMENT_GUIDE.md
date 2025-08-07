# 🚀 Render.com Deployment Guide for UDISE Plus School Scraper

This guide will help you deploy the UDISE Plus School Data Scraper on Render.com with proper configuration for headless browser operation and secret file handling.

## 📋 Prerequisites

1. **Render.com Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Google Sheets Credentials**: Service account JSON file for Google Sheets integration

## 🔧 Deployment Steps

### Step 1: Prepare Your Repository

1. Ensure all files are committed to your GitHub repository:
   - `app.py` - Main Flask application
   - `render.yaml` - Render configuration
   - `requirements.txt` - Python dependencies
   - `render_config.py` - Configuration handler
   - All scraper files (`phase1_statewise_scraper.py`, `sequential_process_state.py`, etc.)

2. **Important**: Do NOT commit `credentials.json` to your repository for security reasons.

### Step 2: Create a New Web Service on Render

1. Go to your Render dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `schools-scraper` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose your preferred region
   - **Branch**: `main` (or your default branch)
   - **Build Command**: 
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     python app.py
     ```

### Step 3: Configure Environment Variables

In the Render dashboard, go to your service → Environment tab and add these variables:

#### Required Environment Variables:
```
HEADLESS=true
RENDER_DEPLOYMENT=true
WINDOW_SIZE=1920,1080
MAX_RETRIES=3
RETRY_DELAY=5
WAIT_BETWEEN_STATES=3
WAIT_BETWEEN_DISTRICTS=2
WAIT_AFTER_SEARCH=5
WAIT_FOR_PAGE_LOAD=3
OUTPUT_DIRECTORY=output
BACKUP_FREQUENCY=100
IMPLICIT_WAIT=10
EXPLICIT_WAIT=10
PAGE_LOAD_TIMEOUT=30
BASE_URL=https://udiseplus.gov.in/#/en/home
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(levelname)s - %(message)s
```

### Step 4: Configure Secret Files

#### For Google Sheets Integration:

1. **Prepare your credentials**:
   - Open your `credentials.json` file
   - Copy the entire JSON content (it should be a single line of JSON)

2. **Add as Environment Variable**:
   - In Render dashboard → Environment tab
   - Add a new environment variable:
     - **Key**: `GOOGLE_CREDENTIALS_JSON`
     - **Value**: Paste the entire JSON content from your credentials.json file
   - Make sure it's marked as "Secret" (🔒 icon)

#### Example credentials format:
```json
{"type":"service_account","project_id":"your-project","private_key_id":"...","private_key":"-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"...","universe_domain":"googleapis.com"}
```

### Step 5: Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy your application
3. Monitor the build logs for any errors
4. Once deployed, you'll get a URL like `https://your-service-name.onrender.com`

## 🌐 Using the Web Interface

Once deployed, you can access your scraper through the web interface:

### Features:
- **Dashboard**: Real-time status and progress monitoring
- **State Selection**: Choose specific states or run all states
- **Live Logs**: View scraper logs in real-time
- **File Management**: Download generated CSV files
- **Progress Tracking**: Visual progress bars and statistics

### Usage:
1. Visit your Render URL
2. Select states to process (or leave empty for all states)
3. Click "Start Scraper"
4. Monitor progress in real-time
5. Download completed CSV files

## 🔧 Configuration Options

### Browser Settings (Optimized for Render):
- **Headless Mode**: Always enabled on Render
- **Window Size**: 1920x1080 (configurable)
- **Memory Optimization**: Enabled for server environments
- **Chrome Flags**: Optimized for headless operation

### Performance Settings:
- **Timeouts**: Balanced for server environment
- **Retry Logic**: 3 attempts with delays
- **Batch Processing**: Optimized for memory usage

## 🐛 Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check that all dependencies are in `requirements.txt`
   - Verify Python version compatibility
   - Check build logs for specific errors

2. **Chrome/Selenium Issues**:
   - Chrome is automatically installed via the build command
   - Headless mode is enforced for server environments
   - Check logs for browser initialization errors

3. **Google Sheets Authentication**:
   - Verify `GOOGLE_CREDENTIALS_JSON` environment variable is set correctly
   - Ensure the service account has access to your Google Sheet
   - Check that the sheet name matches exactly

4. **Memory Issues**:
   - Consider upgrading to a higher Render plan
   - Reduce batch sizes in configuration
   - Monitor memory usage in logs

### Debug Steps:

1. **Check Health Endpoint**:
   ```
   GET https://your-service.onrender.com/health
   ```

2. **View Application Logs**:
   - Go to Render dashboard → Your service → Logs
   - Look for startup messages and error details

3. **Test Configuration**:
   - Verify environment variables are set correctly
   - Check that credentials are properly formatted

## 📊 Monitoring and Maintenance

### Performance Monitoring:
- Monitor CPU and memory usage in Render dashboard
- Check response times and error rates
- Review scraper logs for performance issues

### Data Management:
- CSV files are stored temporarily on the server
- Download important files promptly
- Consider setting up automated backups

### Updates and Maintenance:
- Push updates to your GitHub repository
- Render will automatically redeploy
- Monitor deployment logs for issues

## 🔒 Security Best Practices

1. **Never commit credentials** to your repository
2. **Use environment variables** for all sensitive data
3. **Regularly rotate** service account keys
4. **Monitor access logs** for unusual activity
5. **Keep dependencies updated** for security patches

## 💡 Tips for Success

1. **Start Small**: Test with a few states first
2. **Monitor Resources**: Watch memory and CPU usage
3. **Regular Backups**: Download CSV files regularly
4. **Error Handling**: The scraper continues even if individual states fail
5. **Scaling**: Consider upgrading Render plan for better performance

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Render documentation: [render.com/docs](https://render.com/docs)
3. Check application logs in Render dashboard
4. Verify all environment variables are set correctly

---

**Note**: This deployment is optimized for Render.com's environment with headless browser operation and proper secret file handling. The scraper will automatically detect the Render environment and configure itself accordingly.
