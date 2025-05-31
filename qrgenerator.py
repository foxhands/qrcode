import argparse
import traceback
import sys
import os
from datetime import datetime
import re

try:
    import pyqrcode
    import png
    from pyzbar.pyzbar import decode
    from PIL import Image, ImageDraw
    from colorama import Fore, Style, init
    import svgwrite
except ModuleNotFoundError:
    print("Install missing modules: pip install -r requirements.txt")
    exit(1)

# Initialize colorama for Windows compatibility
init(autoreset=True)


def banner():
    """Display the application banner"""
    return f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
║                    QR Code Generator Pro                 ║
║                        v2.0.0                           ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""


def generate_qr(raw_text='', file_name='', output_format='png', fg_color='black', bg_color='white'):
    """Enhanced QR code generation with multiple formats and colors"""
    try:
        qr_code = pyqrcode.create(raw_text)

        # Display in terminal
        print(qr_code.terminal())

        if output_format.lower() == 'svg':
            # Generate SVG
            svg_buffer = qr_code.svg(scale=10)
            svg_path = f'qrcodes/{file_name}.svg'
            with open(svg_path, 'w') as f:
                f.write(svg_buffer)
            print(f"{Fore.GREEN}✓ SVG saved: {Fore.CYAN}{svg_path}")

        elif output_format.lower() == 'png':
            # Generate colored PNG
            png_path = f'qrcodes/{file_name}.png'

            if fg_color == 'black' and bg_color == 'white':
                # Standard black/white
                qr_code.png(png_path, scale=10)
            else:
                # Custom colors
                generate_colored_qr(qr_code, png_path, fg_color, bg_color)

            print(f"{Fore.GREEN}✓ PNG saved: {Fore.CYAN}{png_path}")

        elif output_format.lower() == 'both':
            # Generate both formats
            svg_path = f'qrcodes/{file_name}.svg'
            png_path = f'qrcodes/{file_name}.png'

            # SVG
            svg_buffer = qr_code.svg(scale=10)
            with open(svg_path, 'w') as f:
                f.write(svg_buffer)

            # PNG
            if fg_color == 'black' and bg_color == 'white':
                qr_code.png(png_path, scale=10)
            else:
                generate_colored_qr(qr_code, png_path, fg_color, bg_color)

            print(f"{Fore.GREEN}✓ Files saved:")
            print(f"  {Fore.CYAN}SVG: {svg_path}")
            print(f"  {Fore.CYAN}PNG: {png_path}")

    except Exception as e:
        print(f"{Fore.RED}❌ Error generating QR code: {str(e)}")
        return False

    return True


def generate_colored_qr(qr_code, output_path, fg_color='black', bg_color='white'):
    """Generate colored QR code using PIL"""
    try:
        # Convert color names to RGB
        color_map = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'purple': (128, 0, 128),
            'orange': (255, 165, 0),
            'pink': (255, 192, 203),
            'cyan': (0, 255, 255),
            'navy': (0, 0, 128),
            'darkgreen': (0, 100, 0)
        }

        fg_rgb = color_map.get(fg_color.lower(), (0, 0, 0))
        bg_rgb = color_map.get(bg_color.lower(), (255, 255, 255))

        # Get QR code matrix
        modules = qr_code.code
        module_count = len(modules)

        # Create image
        scale = 10
        img_size = module_count * scale
        img = Image.new('RGB', (img_size, img_size), bg_rgb)
        draw = ImageDraw.Draw(img)

        # Draw QR modules
        for row in range(module_count):
            for col in range(module_count):
                if modules[row][col]:
                    x1 = col * scale
                    y1 = row * scale
                    x2 = x1 + scale
                    y2 = y1 + scale
                    draw.rectangle([x1, y1, x2, y2], fill=fg_rgb)

        img.save(output_path)

    except Exception as e:
        print(f"{Fore.RED}❌ Error creating colored QR: {str(e)}")
        # Fallback to standard generation
        qr_code.png(output_path, scale=10)


def generate_wifi_qr(ssid, password, security='WPA', hidden=False, file_name=''):
    """Generate WiFi QR code"""
    if not file_name:
        file_name = f"wifi_{ssid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # WiFi QR format: WIFI:T:WPA;S:mynetwork;P:mypass;H:false;;
    hidden_flag = 'true' if hidden else 'false'
    wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden_flag};;"

    print(f"{Fore.YELLOW}📶 Generating WiFi QR code...")
    print(f"   SSID: {Fore.CYAN}{ssid}")
    print(f"   Security: {Fore.CYAN}{security}")
    print(f"   Hidden: {Fore.CYAN}{hidden}")

    return generate_qr(wifi_string, file_name)


def read_qr(file_name):
    """Enhanced QR code reading with better error handling"""
    try:
        if not os.path.exists(file_name):
            print(f"{Fore.RED}❌ File not found: {file_name}")
            return False

        print(f"{Fore.YELLOW}🔍 Scanning QR code...")

        image = Image.open(file_name)
        qr_data = decode(image)

        if not qr_data:
            print(f"{Fore.RED}❌ No QR code found in image")
            return False

        decoded_text = qr_data[0].data.decode("utf-8")
        qr_type = qr_data[0].type

        print(f"{Fore.GREEN}✓ QR Code decoded successfully!")
        print(f"{Fore.GREEN}📝 Content: {Fore.WHITE}{decoded_text}")
        print(f"{Fore.GREEN}📋 Type: {Fore.WHITE}{qr_type}")

        # Detect and parse special QR types
        if decoded_text.startswith('WIFI:'):
            parse_wifi_qr(decoded_text)
        elif decoded_text.startswith('http'):
            print(f"{Fore.BLUE}🌐 URL detected")
        elif decoded_text.startswith('tel:'):
            print(f"{Fore.BLUE}📞 Phone number detected")
        elif decoded_text.startswith('mailto:'):
            print(f"{Fore.BLUE}📧 Email detected")

        return True

    except Exception as e:
        print(f"{Fore.RED}❌ Error reading QR code: {str(e)}")
        return False


def parse_wifi_qr(wifi_string):
    """Parse and display WiFi QR code information"""
    try:
        # Extract WiFi parameters
        parts = wifi_string.replace('WIFI:', '').split(';')
        wifi_info = {}

        for part in parts:
            if ':' in part:
                key, value = part.split(':', 1)
                wifi_info[key] = value

        print(f"{Fore.BLUE}📶 WiFi QR Code detected:")
        print(f"   SSID: {Fore.CYAN}{wifi_info.get('S', 'N/A')}")
        print(f"   Password: {Fore.CYAN}{wifi_info.get('P', 'N/A')}")
        print(f"   Security: {Fore.CYAN}{wifi_info.get('T', 'N/A')}")
        print(f"   Hidden: {Fore.CYAN}{wifi_info.get('H', 'false')}")

    except Exception as e:
        print(f"{Fore.YELLOW}⚠️  Could not parse WiFi details: {str(e)}")


def path_check():
    """Ensure output directory exists"""
    path = "qrcodes"
    if not os.path.exists(path):
        print(f"{Fore.YELLOW}📁 Creating output directory: {path}")
        os.makedirs(path, exist_ok=True)
        print(f"{Fore.GREEN}✓ Directory created")


def validate_input(text):
    """Basic input validation"""
    if not text or not text.strip():
        return False, "Input text cannot be empty"

    if len(text) > 2953:  # QR code limit for alphanumeric
        return False, "Input text is too long for QR code"

    return True, "Valid"


def get_available_colors():
    """Return list of available colors"""
    return ['black', 'white', 'red', 'green', 'blue', 'yellow', 'purple',
            'orange', 'pink', 'cyan', 'navy', 'darkgreen']


def main():
    parser = argparse.ArgumentParser(
        description='QR Code Generator Pro - Create and decode QR codes with advanced features',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  {sys.argv[0]} -i "Hello World"                          # Basic QR code
  {sys.argv[0]} -i "Hello" -o "my_qr" -f svg             # SVG format
  {sys.argv[0]} -i "Hello" --fg red --bg yellow          # Colored QR
  {sys.argv[0]} --wifi "MyNetwork" "MyPassword"          # WiFi QR code
  {sys.argv[0]} -d "qrcodes/my_qr.png"                   # Decode QR code

Available colors: {', '.join(get_available_colors())}
        """
    )

    parser.add_argument('-i', '--input', help='Input text string to convert to QR code')
    parser.add_argument('-o', '--output', help='Custom output filename (without extension)')
    parser.add_argument('-d', '--decode', help='Decode QR code from image file')
    parser.add_argument('-f', '--format', choices=['png', 'svg', 'both'],
                        default='png', help='Output format (default: png)')
    parser.add_argument('--fg', '--foreground', dest='fg_color',
                        choices=get_available_colors(), default='black',
                        help='Foreground color (default: black)')
    parser.add_argument('--bg', '--background', dest='bg_color',
                        choices=get_available_colors(), default='white',
                        help='Background color (default: white)')
    parser.add_argument('--wifi', nargs='+', metavar=('SSID', 'PASSWORD'),
                        help='Generate WiFi QR code: --wifi "Network Name" "Password" [Security] [Hidden]')

    args = parser.parse_args()

    print(banner())

    try:
        # Handle WiFi QR generation
        if args.wifi:
            if len(args.wifi) < 2:
                print(f"{Fore.RED}❌ WiFi QR requires SSID and password")
                print("Usage: --wifi \"NetworkName\" \"Password\" [WPA/WEP/nopass] [true/false]")
                return

            ssid = args.wifi[0]
            password = args.wifi[1]
            security = args.wifi[2] if len(args.wifi) > 2 else 'WPA'
            hidden = args.wifi[3].lower() == 'true' if len(args.wifi) > 3 else False

            file_name = args.output if args.output else f"wifi_{ssid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            if generate_wifi_qr(ssid, password, security, hidden, file_name):
                print(f"{Fore.GREEN}🎉 WiFi QR code generated successfully!")
            return

        # Handle QR decoding
        if args.decode:
            if read_qr(args.decode):
                print(f"{Fore.GREEN}🎉 QR code decoded successfully!")
            return

        # Handle QR generation
        if args.input:
            # Validate input
            is_valid, message = validate_input(args.input)
            if not is_valid:
                print(f"{Fore.RED}❌ {message}")
                return

            file_name = args.output if args.output else datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

            print(f"{Fore.YELLOW}🔄 Generating QR code...")
            print(f"   Text: {Fore.CYAN}{args.input[:50]}{'...' if len(args.input) > 50 else ''}")
            print(f"   Format: {Fore.CYAN}{args.format.upper()}")
            print(f"   Colors: {Fore.CYAN}{args.fg_color} on {args.bg_color}")

            if generate_qr(args.input, file_name, args.format, args.fg_color, args.bg_color):
                print(f"{Fore.GREEN}🎉 QR code generated successfully!")
            return

        # Interactive mode
        print(f"{Fore.BLUE}🎯 Interactive QR Code Generator")
        print(f"{Fore.YELLOW}Choose an option:")
        print("1. Generate text QR code")
        print("2. Generate WiFi QR code")
        print("3. Decode QR code from file")

        choice = input(f"\n{Fore.BLUE}Enter choice (1-3): {Style.RESET_ALL}").strip()

        if choice == '1':
            raw_text = input(f"{Fore.BLUE}Enter text to convert: {Style.RESET_ALL}")
            is_valid, message = validate_input(raw_text)
            if not is_valid:
                print(f"{Fore.RED}❌ {message}")
                return

            file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            if generate_qr(raw_text, file_name):
                print(f"{Fore.GREEN}🎉 QR code generated successfully!")

        elif choice == '2':
            ssid = input(f"{Fore.BLUE}WiFi Network Name (SSID): {Style.RESET_ALL}")
            password = input(f"{Fore.BLUE}WiFi Password: {Style.RESET_ALL}")
            security = input(f"{Fore.BLUE}Security type (WPA/WEP/nopass) [WPA]: {Style.RESET_ALL}") or 'WPA'
            hidden = input(f"{Fore.BLUE}Hidden network? (y/n) [n]: {Style.RESET_ALL}").lower().startswith('y')

            file_name = f"wifi_{ssid}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if generate_wifi_qr(ssid, password, security, hidden, file_name):
                print(f"{Fore.GREEN}🎉 WiFi QR code generated successfully!")

        elif choice == '3':
            file_path = input(f"{Fore.BLUE}Enter path to QR code image: {Style.RESET_ALL}")
            if read_qr(file_path):
                print(f"{Fore.GREEN}🎉 QR code decoded successfully!")
        else:
            print(f"{Fore.RED}❌ Invalid choice")

    except KeyboardInterrupt:
        print(f'\n\n{Fore.RED}👋 Goodbye!')
    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected error: {str(e)}")
        traceback.print_exc()


if __name__ == '__main__':
    path_check()
    main()
