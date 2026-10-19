.PHONY: example build check vendor

example:
	hugo server --source exampleSite --bind 127.0.0.1 --port 1315 --disableFastRender

build:
	hugo --source exampleSite --cleanDestinationDir

check: build
	node --check assets/hugo-content/runtime.js
	python3 tests/smoke.py

vendor:
	npm ci --ignore-scripts
	npm run build

.PHONY: subset-fonts check-font-subsets

subset-fonts:
	uv run --no-project --with fonttools==4.67.0 --with brotli==1.2.0 python scripts/subset-nerd-font.py

check-font-subsets:
	uv run --no-project --with fonttools==4.67.0 --with brotli==1.2.0 python scripts/subset-nerd-font.py --check
