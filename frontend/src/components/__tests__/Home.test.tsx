import React from 'react';
import { render, screen } from '@testing-library/react';
import Home from '../../pages/index';

describe('Home component', () => {
  it('renders the main heading', () => {
    render(<Home />);
    const heading = screen.getByRole('heading', { name: /Welcome to Math LMS/i });
    expect(heading).toBeInTheDocument();
  });

  it('renders the description text', () => {
    render(<Home />);
    const description = screen.getByText(/A specialized Learning Management System/i);
    expect(description).toBeInTheDocument();
  });

  it('renders feature cards', () => {
    render(<Home />);
    expect(screen.getByText(/Interactive Math Content/i)).toBeInTheDocument();
    expect(screen.getByText(/Personalized Learning/i)).toBeInTheDocument();
    expect(screen.getByText(/Comprehensive Analytics/i)).toBeInTheDocument();
  });
});