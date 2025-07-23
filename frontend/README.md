# Mamatoto Frontend

A modern Vue.js application for maternal and child health management.

## Features

- 📱 **Mobile-First Design**: Responsive design optimized for mobile devices
- 🔐 **Secure Authentication**: JWT-based authentication with auto-refresh
- 📊 **Interactive Dashboard**: Real-time health tracking and insights
- 💉 **Vaccination Tracking**: Automated vaccination schedules and reminders
- 📈 **Growth Monitoring**: WHO-standard growth charts and percentile tracking
- 🤖 **AI Health Assistant**: Intelligent chatbot for health queries
- 🌍 **Multilingual Support**: English and Kiswahili language options
- ⚡ **PWA Ready**: Offline support and app-like experience

## Tech Stack

- **Frontend Framework**: Vue 3 with Composition API
- **State Management**: Pinia
- **Routing**: Vue Router 4
- **HTTP Client**: Axios with intercept ors
- **Styling**: Tailwind CSS
- **Charts**: Chart.js with Vue wrapper
- **Build Tool**: Vite
- **Type Safety**: JSDoc comments
- **Testing**: Vitest + Vue Test Utils

## Getting Started

### Prerequisites

- Node.js 16+ and npm
- Backend API running on port 8000

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/mamatoto.git
cd mamatoto/frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev
```

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Lint code
npm run format       # Format code with Prettier
npm run test         # Run tests
```

## Project Structure

```
src/
├── components/          # Reusable Vue components
│   ├── common/         # Common UI components
│   ├── forms/          # Form components
│   └── dashboard/      # Dashboard-specific components
├── views/              # Page-level components
├── stores/             # Pinia stores
├── router/             # Vue Router configuration
├── utils/              # Utility functions
├── composables/        # Vue composition functions
└── assets/             # Static assets
```

## Key Components

### Authentication
- JWT token management with automatic refresh
- Route guards for protected pages
- Persistent login state

### Health Tracking
- Pregnancy week calculation and progress tracking
- Child vaccination schedule management
- Growth percentile calculations using WHO standards
- Health record management with categorization

### User Experience
- Loading states and error handling
- Toast notifications for user feedback
- Responsive design for all screen sizes
- Keyboard navigation support
- Screen reader compatibility

## Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Deploy to Netlify

```bash
# Build the project
npm run build

# Deploy dist/ folder to Netlify
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.