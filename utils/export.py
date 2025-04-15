from typing import Dict, Any, Optional
import json
import plotly
import pandas as pd
from pathlib import Path
from datetime import datetime
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

from .logging import logger

class VisualizationExporter:
    """Handles exporting visualizations in various formats."""
    
    SUPPORTED_FORMATS = {
        'html': 'HTML interactive visualization',
        'png': 'Static PNG image',
        'svg': 'Vector graphics format',
        'pdf': 'PDF document',
        'json': 'Raw JSON data',
        'csv': 'CSV data export'
    }
    
    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the exporter.
        
        Args:
            output_dir (str, optional): Directory to save exported files
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "exports"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export(
        self,
        visualization_data: Dict[str, Any],
        format: str,
        filename: Optional[str] = None
    ) -> str:
        """
        Export visualization in the specified format.
        
        Args:
            visualization_data: The visualization data to export
            format: Export format (html, png, svg, pdf, json, csv)
            filename: Optional custom filename
            
        Returns:
            str: Path to the exported file
        """
        if format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported format: {format}")
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"visualization_{timestamp}"
            
        try:
            if format == 'html':
                return self._export_html(visualization_data, filename)
            elif format in ['png', 'svg', 'pdf']:
                return self._export_image(visualization_data, filename, format)
            elif format == 'json':
                return self._export_json(visualization_data, filename)
            elif format == 'csv':
                return self._export_csv(visualization_data, filename)
                
        except Exception as e:
            logger.error(f"Export error: {str(e)}")
            raise
    
    def _export_html(self, data: Dict[str, Any], filename: str) -> str:
        """Export as interactive HTML."""
        filepath = self.output_dir / f"{filename}.html"
        
        fig = plotly.io.from_json(json.dumps(data['plot_data']))
        plotly.offline.plot(fig, filename=str(filepath), auto_open=False)
        
        return str(filepath)
    
    def _export_image(
        self,
        data: Dict[str, Any],
        filename: str,
        format: str
    ) -> str:
        """Export as static image."""
        filepath = self.output_dir / f"{filename}.{format}"
        
        fig = plotly.io.from_json(json.dumps(data['plot_data']))
        fig.write_image(str(filepath))
        
        return str(filepath)
    
    def _export_json(self, data: Dict[str, Any], filename: str) -> str:
        """Export raw JSON data."""
        filepath = self.output_dir / f"{filename}.json"
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
        return str(filepath)
    
    def _export_csv(self, data: Dict[str, Any], filename: str) -> str:
        """Export data as CSV."""
        filepath = self.output_dir / f"{filename}.csv"
        
        # Extract relevant data based on visualization type
        if 'nodes' in data['plot_data']:
            # Network visualization
            df = pd.DataFrame(data['plot_data']['nodes'])
        elif 'data' in data['plot_data']:
            # Timeline or radar visualization
            df = pd.DataFrame(data['plot_data']['data'])
        else:
            df = pd.DataFrame(data['plot_data'])
            
        df.to_csv(filepath, index=False)
        return str(filepath)
    
    def get_base64_image(
        self,
        data: Dict[str, Any],
        format: str = 'png'
    ) -> str:
        """
        Get base64 encoded image for embedding.
        
        Args:
            data: Visualization data
            format: Image format (png, svg)
            
        Returns:
            str: Base64 encoded image data
        """
        buffer = BytesIO()
        
        fig = plotly.io.from_json(json.dumps(data['plot_data']))
        fig.write_image(buffer, format=format)
        
        image_data = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/{format};base64,{image_data}"
    
    @staticmethod
    def get_supported_formats() -> Dict[str, str]:
        """Get list of supported export formats with descriptions."""
        return VisualizationExporter.SUPPORTED_FORMATS