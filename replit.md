# Rational Function Graph Game

## Overview

This is an interactive educational game built with Streamlit that teaches students how to graph rational functions. The application helps students identify key features of rational functions including vertical and horizontal asymptotes, holes, intercepts, and end behavior through gamified learning experiences.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based web application
- **UI Components**: Interactive widgets including sliders, text inputs, buttons, and multiselect dropdowns
- **Visualization**: Matplotlib for plotting rational functions and their features
- **Layout**: Wide layout with sidebar for game controls and main content area for function analysis

### Backend Architecture
- **Core Logic**: Object-oriented Python architecture with three main classes:
  - `RationalAnalyzer`: Handles mathematical analysis of rational functions
  - `GameModes`: Manages different game modes and difficulty levels
  - Main application logic in `app.py`

### State Management
- **Session State**: Streamlit session state for maintaining game progress including:
  - Player score and level
  - Current game mode
  - Active function analysis
  - Achievement tracking

## Key Components

### RationalAnalyzer Class
- **Purpose**: Mathematical engine for analyzing rational functions
- **Core Functions**:
  - Parse numerator and denominator strings using SymPy
  - Find vertical asymptotes by solving denominator = 0
  - Calculate horizontal asymptotes based on degree comparison
  - Identify holes vs. true asymptotes
  - Generate function graphs with highlighted features

### GameModes Class
- **Purpose**: Manages different learning game modes
- **Difficulty System**: 4-level progression with increasing complexity and point multipliers
- **Game Types**:
  - Function Input Mode: Students enter custom functions
  - Feature Quiz: Identification challenges
  - Graph Builder: Step-by-step construction
  - End Behavior Race: Timed challenges

### Main Application (app.py)
- **Purpose**: Orchestrates the overall user experience
- **Features**:
  - Game dashboard with score tracking
  - Mode selection interface
  - Achievement system
  - Progressive difficulty scaling

## Data Flow

1. **User Input**: Student enters rational function components (numerator/denominator)
2. **Validation**: RationalAnalyzer validates and parses the mathematical expressions
3. **Analysis**: Mathematical features are calculated (asymptotes, holes, intercepts)
4. **Visualization**: Matplotlib generates interactive graphs with highlighted features
5. **Feedback**: Real-time analysis results and scoring
6. **State Update**: Session state updated with score, level, and progress

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework and UI components
- **SymPy**: Symbolic mathematics for function parsing and analysis
- **NumPy**: Numerical computations for plotting
- **Matplotlib**: Graph generation and visualization
- **Random**: Function generation for challenges

### Mathematical Dependencies
- SymPy handles symbolic math operations, equation solving, and calculus
- NumPy provides numerical array operations for plotting data
- Matplotlib creates interactive plots with customizable features

## Deployment Strategy

### Platform
- **Target**: Replit environment
- **Architecture**: Single-page Streamlit application
- **Dependencies**: All managed through Python package manager

### Scalability Considerations
- Session state management for multiple concurrent users
- Matplotlib figure memory management for performance
- Modular class structure allows easy feature expansion

### Development Approach
- Object-oriented design for maintainability
- Separation of concerns (analysis, game logic, UI)
- Error handling for invalid mathematical expressions
- Progressive enhancement with achievement system

## Technical Notes

- The application uses symbolic mathematics (SymPy) for precise mathematical analysis
- Graph rendering is handled server-side with Matplotlib
- Session state persistence maintains game progress across interactions
- The modular design allows easy addition of new game modes and features