# styles.py

def get_styles():
    return """
    <style>
        /* Global Reset */
        [data-testid="stHeader"] { display: none !important; }
        .block-container { padding: 0 !important; max-width: 100%; }

        /* Navbar Styling */
        .navbar { 
            background-color: #4a148c; 
            padding: 15px 5%; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            color: white; 
            font-family: sans-serif;
            position: relative; 
            z-index: 10000; 
        }
        .nav-logo { font-size: 26px; font-weight: bold; }
        .nav-logo span { color: #ffab40; margin-left: 2px; }
        .nav-right { display: flex; align-items: center; gap: 25px; }

        /* Dropdown Menu - The Locked Anchor */
        .nav-item-dropdown { position: relative; display: inline-block; cursor: pointer; }
        .mega-menu {
            display: none; 
            position: absolute; 
            top: 100%; 
            left: 0; 
            width: 800px; 
            background: white; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            z-index: 9999;
            padding: 20px;
            border-radius: 0 0 12px 12px;
            border: 1px solid #ddd;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
        }
        .nav-item-dropdown:hover .mega-menu { display: grid; }
        
        /* Typography */
        .mega-title { color: #4a148c; font-weight: 800; font-size: 13px; border-bottom: 2px solid #ffab40; padding-bottom: 5px; }
        .mega-link { color: #555; text-decoration: none; font-size: 12px; display: block; margin: 4px 0; }
        .mega-link:hover { color: #ffab40; font-weight: bold; }

        /* Action Blocks Row */
        .action-blocks-row {
            display: flex;
            justify-content: center;
            gap: 30px;
            padding: 40px 5%;
        }
        .action-block {
            display: flex;
            align-items: center;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 1px solid #eee;
            cursor: pointer;
            overflow: hidden;
            transition: 0.3s;
        }
        .action-block:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
        .action-block-icon { background: #00897b; color: white; padding: 20px; }
        .action-block-label { padding: 20px 30px; font-weight: 800; color: #00897b; }
    </style>
    """
