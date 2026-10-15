[private]
default:
  @just --list

# Install dependencies
install:
  npm install

# Start the development server with hot reload
dev:
  npm run dev

# Build the static site into dist/
build:
  npm run build

# Serve the built site locally
preview:
  npm run preview

# Run the unit tests, the type check, a build and the link check
check:
  npm test
  npm run check
  npm run build
  npm run check-links

# Remove build output
clean:
  rm -rf dist .astro
