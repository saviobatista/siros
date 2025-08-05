# SIROS Flight Movement Prediction System

> **⚠️ ARCHIVED REPOSITORY**  
> This repository is now archived as ANAC has provided official web services at [https://sas.anac.gov.br/sas/siros_api](https://sas.anac.gov.br/sas/siros_api). Web crawling is no longer necessary for retrieving SIROS data.

A Python-based web crawler and analysis system for capturing and processing flight information from Brazil's ANAC SIROS database (https://siros.anac.gov.br/). The system provides accurate flight movement predictions and operational position recommendations for air traffic control planning.

**Note**: This project demonstrates web scraping techniques but is no longer actively maintained due to the availability of official ANAC APIs.

## 🎯 Features

- **Automated Data Collection**: Web scraping from SIROS database using Selenium *(deprecated)*
- **Flight Movement Analysis**: Hourly flight predictions with 99.2% statistical accuracy (T-5 hours)
- **Operational Planning**: Automated position staffing recommendations based on traffic volume
- **Flexible Scheduling**: Configurable work shifts and time periods
- **Multiple Rule Sets**: Different operational rules for various scenarios (normal, pandemic, general)
- **Data Validation**: Built-in integrity checks with MD5 verification
- **Educational Value**: Demonstrates web scraping, data processing, and aviation analytics techniques

## 🚀 Key Capabilities

1. **Hourly Flight Listings**: Movement forecasts by hour for any aerodrome
2. **Shift-Based Analysis**: Flight predictions for specific work shifts
3. **Position Planning**: Automated recommendations for operational positions based on traffic volume
4. **Educational Demonstration**: Web scraping, data processing, and aviation analytics techniques

## 📋 Requirements

```
python >= 3.7
selenium >= 4.0.0
chrome/chromium browser
chromedriver
```

> **Note**: This project is archived and primarily serves as an educational example of web scraping and data processing techniques.

## 🛠️ Installation

> **⚠️ ARCHIVED PROJECT**  
> This installation guide is provided for educational purposes only. For production use, consider using the official ANAC API at [https://sas.anac.gov.br/sas/siros_api](https://sas.anac.gov.br/sas/siros_api).

1. **Clone the repository**:
```bash
git clone <repository-url>
cd siros
```

2. **Install Python dependencies**:
```bash
pip install selenium
```

3. **Install ChromeDriver**:
   - Download from https://chromedriver.chromium.org/
   - Ensure it's in your PATH or place in project directory

4. **Verify Chrome/Chromium installation**:
   - The system uses headless Chrome for web scraping

## ⚙️ Configuration

### Basic Configuration

Edit `siros.py` to configure your setup:

```python
# Set your target aerodrome (ICAO code)
aerodromo = 'SBKP'  # Viracopos (default)

# Configure work shifts (24-hour format)
previsao.setTurnos(
    turnos=[7, 15, 23],  # Shift start times: 07:00, 15:00, 23:00
    duracao=8            # 8-hour shifts
)

# Data retention
robot.maintain = False  # Set to True to keep downloaded CSV files
```

### Shift Configuration Examples

```python
# Standard 3-shift operation
previsao.setTurnos(turnos=[7, 15, 23], duracao=8)

# 2-shift operation
previsao.setTurnos(turnos=[6, 18], duracao=12)

# Custom shifts
previsao.setTurnos(turnos=[8, 20], duracao=10)
```

## 🚀 Usage

> **⚠️ EDUCATIONAL USE ONLY**  
> This system demonstrates web scraping techniques but is no longer recommended for production use due to the availability of official ANAC APIs.

### Basic Usage

```bash
python siros.py
```

This will:
1. Connect to SIROS website *(may fail due to website changes)*
2. Download flight data for today and tomorrow *(or use sample data)*
3. Generate three reports:
   - General hourly movement forecast
   - Next shift movement forecast
   - Operational position recommendations

### Advanced Usage

#### Using Different Aerodromes

```python
from lib.siros_parser import SirosParser
from lib.previsao import Previsao
from lib.rules import RulesBita

# Configure for different aerodrome
aerodromo = 'SBGR'  # Guarulhos
robot = SirosParser(aerodromo)
# ... rest of configuration
```

#### Custom Date Ranges

```python
from datetime import datetime, timedelta

# Specific date range
start_date = datetime(2024, 1, 15)
end_date = datetime(2024, 1, 16)

voos = robot.parse(
    begin=start_date.strftime('%d/%m/%Y'),
    end=end_date.strftime('%d/%m/%Y')
)
```

#### Testing with Sample Data

```python
# Use included sample CSV instead of live data
voos = robot.parseCSV('modelo.csv')
```

## 📊 Output Examples

### Hourly Movement Forecast
```
PREVISAO DE MOVIMENTO
+========== 15/01/2024 =========+
| HORA  | ARR | DEP | TOTAL |
+-------------------------------+
| 6:00  | 2   | 3   | 5     |
| 7:00  | 5   | 4   | 9     |
| 8:00  | 8   | 6   | 14    |
+-------------------------------+
```

### Shift Analysis
```
PREVISAO DE MOVIMENTO PARA O TURNO
+===== 15/01 07:00 - 15:00 ====+
| HORA  | ARR | DEP | TOTAL |
+-------------------------------+
| 7:00  | 5   | 4   | 9     |
| 8:00  | 8   | 6   | 14    |
+-------------------------------+
```

### Position Planning
```
PREVISÃO DE DISTRIBUIÇÃO DE POSIÇÕES OPERACIONAIS
+========== TURNO: 15/01/2024 07:00 ATÉ 15/01/2024 15:00 =======+
| HORA  | ARR | DEP | TOTAL | POSIÇÕES              |
+---------------------------------------------------------------+
| 7:00  | 5   | 4   | 9     | TWR  GND              |
| 8:00  | 8   | 6   | 14    | TWR  GND  CLR  CORD  SUP |
+---------------------------------------------------------------+
```

## 🏗️ Architecture

### Core Components

#### 1. **SirosParser** (`lib/siros_parser.py`)
- Web scraping engine using Selenium
- Handles SIROS website interaction
- CSV download and validation
- Data integrity verification with MD5 checksums

#### 2. **Voo** (`lib/voo.py`)
- Flight data model
- Automatic ARR/DEP classification
- Time zone and schedule handling
- Clearance time adjustments (-20 min for departures)

#### 3. **Previsao** (`lib/previsao.py`)
- Movement prediction engine
- Hourly traffic binning
- Shift calculation and management
- Report generation

#### 4. **Rules Engine** (`lib/rules.py`)
- Position staffing algorithms
- Multiple rule sets (Bita, Pandemia, Geral)
- Configurable staffing thresholds

### Data Flow

```
SIROS Website → Selenium → CSV Download → Flight Objects → 
Hourly Binning → Movement Analysis → Rule Application → Reports
```

## 📚 API Documentation

### SirosParser Class

```python
class SirosParser:
    def __init__(self, aerodromo: str)
    def parse(self, begin: str, end: str) -> List[Voo]
    def parseCSV(self, arquivo: str) -> List[Voo]
```

### Previsao Class

```python
class Previsao:
    def __init__(self, aerodromo: str)
    def setTurnos(self, turnos: List[int], duracao: int)
    def parseVoos(self, voos: List[Voo])
    def dump()  # General forecast
    def dump_turno()  # Shift forecast
    def dump_distribuicao(rules: Rules)  # Position planning
```

### Rules Classes

```python
class Rules(ABC):
    @abstractmethod
    def test(movimentos: dict) -> str

class RulesBita(Rules):
    # Main operational rules
    
class RulesPandemia(Rules):
    # Pandemic-era reduced staffing
    
class RulesGeral(Rules):
    # General purpose rules
```

## 🎯 Position Codes

| Code | Position | Description |
|------|----------|-------------|
| TWR | Tower | Air traffic control tower |
| ASSTWR | Assistant Tower | Tower assistant controller |
| GND | Ground | Ground movement control |
| CLR | Clearance | Clearance delivery |
| ASSCLR | Assistant Clearance | Clearance assistant |
| CORD | Coordinator | Traffic coordinator |
| SUP | Supervisor | Shift supervisor |

## 🔧 Operational Rules

### RulesBita (Primary)
- **Base**: TWR always required
- **Ground**: GND when total movements ≥ 8
- **Departures**: 
  - \>14: Full departure team (CLR, ASSCLR, CORD, SUP)
  - \>10: Reduced team (CLR, CORD, SUP)
- **Assistant Tower**: 
  - Required when total > 20 movements
  - Or when > 5 movements with minimal staffing

### RulesPandemia (COVID-19)
- Simplified staffing model
- \>10 departures: TWR, GND, CLR, SUP
- ≤10 departures: TWR, GND only

### RulesGeral (General)
- \>15 total movements: Full team
- \>7 departures: TWR, GND, CLR
- ≤7 departures: TWR, GND only

## 🔍 Troubleshooting

### Common Issues

1. **ChromeDriver not found**
   ```bash
   # Ensure ChromeDriver is in PATH or install via:
   brew install chromedriver  # macOS
   apt-get install chromium-chromedriver  # Ubuntu
   ```

2. **SIROS website changes**
   - Check MD5 validation errors
   - Verify CSV format compatibility
   - Update selectors if needed

3. **Download timeout**
   - Increase timeout in `SirosParser`
   - Check network connectivity
   - Verify SIROS site availability

4. **Data accuracy issues**
   - System accuracy degrades beyond T-5 hours
   - Verify aerodrome code is correct
   - Check date format (DD/MM/YYYY)

## 📝 File Structure

```
siros/
├── siros.py              # Main entry point
├── modelo.csv            # Sample data for testing
├── lib/
│   ├── siros_parser.py   # Web scraping engine
│   ├── voo.py           # Flight data model
│   ├── previsao.py      # Prediction engine
│   └── rules.py         # Staffing rules
└── tmp/                 # Temporary download directory
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Update MD5 checksums if CSV format changes
- Test with multiple aerodromes

## ⚠️ Important Notes

- **Archived Status**: This repository is archived and no longer actively maintained
- **Official API Available**: ANAC now provides official web services at [https://sas.anac.gov.br/sas/siros_api](https://sas.anac.gov.br/sas/siros_api)
- **Educational Purpose**: This project demonstrates web scraping, data processing, and aviation analytics techniques
- **Accuracy**: 99.2% statistical accuracy for T-5 hour predictions *(historical reference)*
- **Legal**: Ensure compliance with SIROS terms of service *(when using web scraping)*
- **Rate Limiting**: Be respectful of SIROS server resources *(when using web scraping)*
- **Data Retention**: Configure `maintain` flag based on privacy requirements

## 📄 License

This project is provided for **educational purposes only**. The repository is archived and no longer actively maintained. For production use, please consider using the official ANAC API at [https://sas.anac.gov.br/sas/siros_api](https://sas.anac.gov.br/sas/siros_api).

## 🔄 Migration to Official API

ANAC has provided official web services that replace the need for web scraping:

- **Official API**: [https://sas.anac.gov.br/sas/siros_api](https://sas.anac.gov.br/sas/siros_api)
- **Benefits**: More reliable, structured data, better performance
- **Recommendation**: Use official APIs for production applications

## 🆘 Support

> **⚠️ ARCHIVED REPOSITORY**  
> This project is no longer actively maintained. For current support:

For issues related to:
- **Official API**: Contact ANAC through [https://sas.anac.gov.br/sas/siros_api](https://sas.anac.gov.br/sas/siros_api)
- **Educational questions**: Review the code for learning web scraping techniques
- **Historical reference**: This project demonstrates aviation data processing methods

---

**Statistical Accuracy**: 99.2% for T-5 hour predictions based on historical validation data *(archived reference)*.