#!/usr/bin/env python3
"""
Examples of using the plot regenerator for different visualization styles
"""

from regenerate_plots import PlotRegenerator
import os

def example_basic_regeneration():
    """Basic example of regenerating plots."""
    print("📊 Example: Basic Plot Regeneration")
    print("=" * 40)
    
    # Find the most recent data file
    data_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.csv', '.json')) and 'jailbreaking' in file:
                data_files.append(os.path.join(root, file))
    
    if not data_files:
        print("❌ No data files found. Run the scraper first to generate data.")
        return
    
    # Use the most recent file
    data_file = data_files[-1]
    print(f"Using data file: {data_file}")
    
    # Initialize regenerator
    regenerator = PlotRegenerator()
    
    # Load data
    if regenerator.load_data(data_file):
        # Generate plots with default style
        regenerator.generate_visualizations('outputs/basic_plots')
        print("✅ Basic plots generated!")

def example_custom_styles():
    """Example with different plot styles."""
    print("\n📊 Example: Custom Plot Styles")
    print("=" * 40)
    
    # Find data file
    data_files = [f for f in os.listdir('.') if f.endswith(('.csv', '.json')) and 'jailbreaking' in f]
    if not data_files:
        print("❌ No data files found.")
        return
    
    data_file = data_files[0]
    regenerator = PlotRegenerator()
    
    if regenerator.load_data(data_file):
        # Generate plots with different styles
        styles = ['default', 'minimal', 'dark']
        
        for style in styles:
            print(f"Generating {style} style plots...")
            regenerator.generate_visualizations(f'outputs/{style}_style', style)
        
        print("✅ All style variations generated!")

def example_custom_formatting():
    """Example with custom formatting parameters."""
    print("\n📊 Example: Custom Formatting")
    print("=" * 40)
    
    # Find data file
    data_files = [f for f in os.listdir('.') if f.endswith(('.csv', '.json')) and 'jailbreaking' in f]
    if not data_files:
        print("❌ No data files found.")
        return
    
    data_file = data_files[0]
    regenerator = PlotRegenerator()
    
    if regenerator.load_data(data_file):
        # Apply custom styling
        style_config = {
            'figure_size': (14, 10),
            'dpi': 400,
            'font_size': 12
        }
        regenerator.customize_plot_style(style_config)
        
        # Generate high-quality plots
        regenerator.generate_visualizations('outputs/high_quality')
        print("✅ High-quality plots generated!")

def example_iterative_development():
    """Example showing iterative plot development."""
    print("\n📊 Example: Iterative Development")
    print("=" * 40)
    
    # Find data file
    data_files = [f for f in os.listdir('.') if f.endswith(('.csv', '.json')) and 'jailbreaking' in f]
    if not data_files:
        print("❌ No data files found.")
        return
    
    data_file = data_files[0]
    regenerator = PlotRegenerator()
    
    if regenerator.load_data(data_file):
        # Iteration 1: Default style
        print("Iteration 1: Default style")
        regenerator.generate_visualizations('outputs/iteration1')
        
        # Iteration 2: Minimal style
        print("Iteration 2: Minimal style")
        regenerator.generate_visualizations('outputs/iteration2', 'minimal')
        
        # Iteration 3: Custom formatting
        print("Iteration 3: Custom formatting")
        style_config = {
            'figure_size': (16, 12),
            'dpi': 300,
            'font_size': 14
        }
        regenerator.customize_plot_style(style_config)
        regenerator.generate_visualizations('outputs/iteration3')
        
        print("✅ Iterative development completed!")

def main():
    print("🚀 Plot Regenerator Examples")
    print("=" * 50)
    
    # Run examples
    example_basic_regeneration()
    example_custom_styles()
    example_custom_formatting()
    example_iterative_development()
    
    print("\n✅ All examples completed!")
    print("\n💡 Tips for iterative development:")
    print("  1. Use --data-file to specify your data")
    print("  2. Use --style to try different styles")
    print("  3. Use --figure-size to adjust plot dimensions")
    print("  4. Use --dpi to control image quality")
    print("  5. Use --output-dir to organize different versions")

if __name__ == "__main__":
    main() 