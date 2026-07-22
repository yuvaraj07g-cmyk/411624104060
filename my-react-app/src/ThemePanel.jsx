function ThemePanel({ theme, toggleTheme }) {
  return (
    <div>
      <p>Current Theme: {theme}</p>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </div>
  );
}

export default ThemePanel;