#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to install dependencies
install_deps() {
    echo -e "${GREEN}Installing dependencies...${NC}"
    npm install
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Dependencies installed successfully${NC}"
    else
        echo -e "${RED}Failed to install dependencies${NC}"
        exit 1
    fi
}

# Function to clean node_modules and reinstall
clean_install() {
    echo -e "${YELLOW}Cleaning node_modules...${NC}"
    rm -rf node_modules package-lock.json
    install_deps
}

# Function to check and install missing dependencies
check_deps() {
    echo -e "${GREEN}Checking for missing dependencies...${NC}"
    missing_deps=()

    # Check for required npm packages
    required_packages=("axios" "cheerio" "express" "dotenv")
    for package in "${required_packages[@]}"; do
        if ! npm list | grep -q "^[└├]── $package@"; then
            missing_deps+=("$package")
        fi
    done

    # Install missing dependencies if any
    if [ ${#missing_deps[@]} -ne 0 ]; then
        echo -e "${YELLOW}Missing dependencies found: ${missing_deps[*]}${NC}"
        echo -e "Installing missing packages..."
        npm install "${missing_deps[@]}"
    else
        echo -e "${GREEN}All dependencies are installed${NC}"
    fi
}

# Function to run linting
lint() {
    echo -e "${GREEN}Running linter...${NC}"
    if [ -f "node_modules/.bin/eslint" ]; then
        ./node_modules/.bin/eslint src/ --fix
    else
        echo -e "${YELLOW}ESLint not found. Installing...${NC}"
        npm install eslint --save-dev
        ./node_modules/.bin/eslint src/ --fix
    fi
}

# Function to create a backup of the current state
backup() {
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_dir="backups/backup_${timestamp}"
    echo -e "${GREEN}Creating backup in ${backup_dir}...${NC}"
    mkdir -p "$backup_dir"
    cp -r src/ config/ package.json "$backup_dir"
    echo -e "${GREEN}Backup created successfully${NC}"
}

# Function to check server health
check_health() {
    echo -e "${GREEN}Checking server health...${NC}"
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/health)
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}Server is healthy${NC}"
    else
        echo -e "${RED}Server is not responding properly (Status: $response)${NC}"
    fi
}

# Function to show logs
show_logs() {
    if [ -d "logs" ]; then
        echo -e "${GREEN}Recent logs:${NC}"
        find logs -type f -name "*.log" -mtime -1 -exec tail -n 50 {} \;
    else
        echo -e "${YELLOW}No logs directory found${NC}"
    fi
}

# Function to setup development environment
setup_dev() {
    echo -e "${GREEN}Setting up development environment...${NC}"
    install_deps

    # Create necessary directories
    mkdir -p logs backups

    # Setup git hooks if .git exists
    if [ -d ".git" ]; then
        cp scripts/pre-commit.sh .git/hooks/pre-commit
        chmod +x .git/hooks/pre-commit
    fi

    # Create .env if it doesn't exist
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}Creating .env file...${NC}"
        cp config/.env.example .env
    fi
}

# Function to deploy the application
deploy() {
    echo -e "${GREEN}Deploying application...${NC}"
    echo -e "${GREEN}Checking for missing dependencies before deploy...${NC}"
    check_deps
    echo -e "${YELLOW}Pulling latest code from Git...${NC}"
    git pull origin main
    echo -e "${GREEN}Installing dependencies...${NC}"
    npm install

    echo -e "${GREEN}Building project...${NC}"
    if grep -q '"build":' package.json; then
        npm run build || { echo -e "${RED}Build failed. Aborting deploy.${NC}"; exit 1; }
    else
        echo -e "${YELLOW}No build script found in package.json, skipping build step.${NC}"
    fi

    echo -e "${GREEN}Restarting server...${NC}"
    if command -v pm2 &> /dev/null; then
        pm2 restart all
    else
        echo -e "${YELLOW}PM2 not found. Please install PM2 globally (npm install -g pm2) if you want server restart automation.${NC}"
    fi
    echo -e "${GREEN}Deployment completed successfully${NC}"
}

# Function to test json-parser.sh
test_json_parser() {
    echo -e "${GREEN}Testing json-parser.sh...${NC}"
    ./json-parser.sh '{"name": "Cursor", "version": "1.0.0"}'
}

# Main script logic
case "$1" in
    install)
        install_deps
        ;;
    clean)
        clean_install
        ;;
    check)
        check_deps
        ;;
    lint)
        lint
        ;;
    backup)
        backup
        ;;
    health)
        check_health
        ;;
    logs)
        show_logs
        ;;
    setup)
        setup_dev
        ;;
    deploy)
        deploy
        ;;
    test-json)
        test_json_parser
        ;;
    *)
        echo "Usage: $0 {install|clean|check|lint|backup|health|logs|setup|deploy|test-json}"
        echo "  install: Install dependencies"
        echo "  clean: Remove node_modules and reinstall"
        echo "  check: Check for missing dependencies"
        echo "  lint: Run linter"
        echo "  backup: Create a backup of current state"
        echo "  health: Check server health"
        echo "  logs: Show recent logs"
        echo "  setup: Setup development environment"
        echo "  deploy: Deploy the application (pulls latest code, installs deps, builds, and restarts server)"
        echo "  test-json: Test the JSON parser script (json-parser.sh)"
        exit 1
        ;;
esac

exit 0