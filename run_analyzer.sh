#!/bin/bash
# Run YouTube Success Analyzer with proxy settings cleared
# This ensures no proxy interference from system settings

# Clear any proxy environment variables
unset http_proxy
unset https_proxy
unset HTTP_PROXY
unset HTTPS_PROXY
unset all_proxy
unset ALL_PROXY
unset no_proxy
unset NO_PROXY

# Run the analyzer
python3 youtube_success_analyzer.py "$@"
