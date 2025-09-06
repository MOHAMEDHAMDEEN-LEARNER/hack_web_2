# Development Server Troubleshooting Guide

## Why `npm run dev` May Not Work Consistently

### 1. **Port Conflicts (Most Common)**
**Problem**: Port 3001 is already in use by another process
**Symptoms**: 
- Error: `EADDRINUSE: address already in use 0.0.0.0:3001`
- Server fails to start

**Solutions**:
```bash
# Option 1: Use the safe startup script
./start-dev.sh

# Option 2: Use the safe dev command
npm run dev-safe

# Option 3: Kill processes manually
npm run kill-port
npm run dev

# Option 4: Check what's using the port
lsof -ti:3001
kill -9 [PID]
```

### 2. **Suspended Processes**
**Problem**: Server was suspended with Ctrl+Z instead of properly stopped
**Symptoms**: 
- Process shows status "T" (suspended)
- Port appears in use but no active server

**Solutions**:
```bash
# Find suspended processes
jobs
# Kill suspended processes
kill %1  # or kill -9 [PID]
# Or use our kill script
npm run kill-port
```

### 3. **Environment Variables Not Loaded**
**Problem**: DATABASE_URL or other env vars not set
**Symptoms**:
- Database connection errors
- Missing configuration errors

**Solutions**:
```bash
# Check if .env file exists
ls -la .env

# Use the startup script (automatically loads env vars)
./start-dev.sh

# Or manually export environment variables
export $(cat .env | grep -v '^#' | xargs)
npm run dev
```

### 4. **Node Modules Cache Issues**
**Problem**: Corrupted cache or outdated dependencies
**Symptoms**:
- Unexpected build errors
- Module resolution errors

**Solutions**:
```bash
# Clean everything
npm run clean

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### 5. **Database Connection Issues**
**Problem**: Database not accessible or credentials invalid
**Symptoms**:
- Server starts but database operations fail
- Connection timeout errors

**Solutions**:
```bash
# Check database URL format
echo $DATABASE_URL

# Test database connection
npm run db:push
```

## Recommended Startup Methods

### **Method 1: Reliable Startup Script (Recommended)**
```bash
./start-dev.sh
```
- Automatically handles port conflicts
- Validates environment variables
- Provides clear status messages

### **Method 2: Safe Dev Command**
```bash
npm run dev-safe
```
- Kills any processes on the port first
- Then starts the dev server

### **Method 3: Manual Startup**
```bash
# 1. Kill any existing processes
npm run kill-port

# 2. Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# 3. Start server
npm run dev
```

## Prevention Tips

1. **Always use Ctrl+C** to stop the server, never Ctrl+Z
2. **Use the startup script** for consistent behavior
3. **Check port availability** before starting
4. **Keep environment variables in .env** file
5. **Regular cleanup** with `npm run clean`

## Quick Fix Commands

```bash
# Emergency fix - kills everything and restarts
npm run kill-port && npm run clean && npm install && ./start-dev.sh

# Quick restart
npm run dev-safe

# Check if server is running
curl -I http://localhost:3001/
```
