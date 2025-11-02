# Copilot Instructions for OKRealignment Project

## Project Overview
This is a web mapping application using Mapbox GL JS for Oklahoma realignment visualization.

## Technologies
- HTML5
- Mapbox GL JS v3.0.1
- JavaScript (ES6+)

## Development Guidelines

### Code Style
- Use 4 spaces for indentation
- Use semicolons in JavaScript
- Use single quotes for JavaScript strings
- Use descriptive variable and function names

### Mapbox Best Practices
- Always check if map is loaded before adding layers or sources
- Use `map.on('load', callback)` for initialization code
- Clean up event listeners when removing features
- Cache GeoJSON data when possible for better performance

### File Organization
- Keep HTML, CSS, and JavaScript separate when project grows
- Consider creating `/js`, `/css`, and `/data` folders for larger projects
- Store GeoJSON data files in `/data` directory

### Testing
- Test in multiple browsers (Chrome, Firefox, Edge)
- Test responsive behavior on mobile devices
- Verify map loads correctly with valid access token

### Security
- Never commit Mapbox access tokens to version control
- Use environment variables or config files for sensitive data
- Consider token restrictions in Mapbox account settings

## Common Tasks

### Adding a New Layer
```javascript
map.addLayer({
    id: 'layer-id',
    type: 'line', // or 'fill', 'circle', 'symbol', etc.
    source: 'source-id',
    paint: {
        // Paint properties
    }
});
```

### Loading External GeoJSON
```javascript
map.addSource('source-id', {
    type: 'geojson',
    data: 'path/to/data.geojson'
});
```

### Adding Interactivity
```javascript
map.on('click', 'layer-id', (e) => {
    // Handle click event
});
```

## Resources
- [Mapbox GL JS Documentation](https://docs.mapbox.com/mapbox-gl-js/guides/)
- [Mapbox Examples](https://docs.mapbox.com/mapbox-gl-js/example/)
