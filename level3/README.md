# Level 3 - Advanced Python Tasks

This directory contains three advanced Python programming tasks that demonstrate web frameworks, cryptography, and algorithmic problem-solving.

## Task 1: Django Web Application with Authentication (`django_auth_app/`)

A complete Django web application implementing user authentication, registration, and profile management.

### Features:
- User registration with email validation
- Secure login/logout functionality
- Password reset via email
- Role-based permissions (Admin, Regular User)
- Profile management system
- Django admin interface
- Responsive Bootstrap UI
- CSRF protection and security features

### Setup and Installation:

1. **Automated setup:**
   ```bash
   cd django_auth_app
   python setup_django_project.py
   ```

2. **Manual setup:**
   ```bash
   # Install dependencies
   pip install django django-crispy-forms crispy-bootstrap5
   
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   
   # Start development server
   python manage.py runserver
   ```

### Project Structure:
```
django_auth_app/
 manage.py
 auth_project/
    settings.py      # Django configuration
    urls.py          # URL routing
    wsgi.py
 accounts/
    models.py        # User profile models
    views.py         # Authentication views
    forms.py         # Registration/profile forms
    urls.py          # App URL routing
    admin.py         # Admin configuration
 templates/
    base.html        # Base template
    home.html        # Homepage
    accounts/        # Authentication templates
 static/
     css/             # Stylesheets
```

### Key Features:

#### User Registration:
```python
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
```

#### Authentication Views:
- **Registration**: Custom form with extended user fields
- **Login**: Django's built-in LoginView with custom template
- **Password Reset**: Complete email-based password reset flow
- **Profile Management**: User can update personal information

#### Security Features:
- Password hashing with Django's built-in system
- CSRF protection on all forms
- Session management
- Permission-based access control
- Secure password reset tokens

### Access the Application:
- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Registration**: http://127.0.0.1:8000/accounts/register/
- **Login**: http://127.0.0.1:8000/accounts/login/

## Task 2: File Encryption/Decryption (`file_encryption.py`)

A comprehensive file encryption tool supporting both educational and secure encryption methods.

### Prerequisites:
```bash
pip install cryptography
```

### Features:
- **Caesar Cipher**: Educational encryption with brute-force decryption
- **Fernet Encryption**: Industry-standard symmetric encryption
- Password-based key derivation (PBKDF2)
- Support for text and binary files
- Automatic encryption metadata storage
- Secure salt generation and storage

### How to run:
```bash
python file_encryption.py
```

### Encryption Methods:

#### 1. Caesar Cipher (Educational):
```
 Choose encryption method:
1.  Caesar Cipher (simple, educational)
2.  Fernet Encryption (secure, recommended)
Enter your choice (1-2): 1

Enter shift value (1-25, default=13): 5
 File encrypted with Caesar cipher (shift=5): document.txt.caesar_encrypted
 Encryption info saved: document.txt.caesar_encrypted.caesar_info
```

#### 2. Fernet Encryption (Secure):
```
Enter your choice (1-2): 2
Enter password for encryption: [hidden]
 File encrypted with Fernet: document.txt.fernet_encrypted
 Salt saved: document.txt.fernet_encrypted.salt  
 Encryption info saved: document.txt.fernet_encrypted.fernet_info
```

### Key Features:

#### Caesar Cipher:
- Variable shift values (1-25)
- Preserves non-alphabetic characters
- Brute-force decryption assistance
- Educational value for learning encryption concepts

#### Fernet Encryption:
- AES 128 encryption in CBC mode
- HMAC for authentication
- Password-based key derivation with PBKDF2
- Random salt generation (16 bytes)
- 100,000 iterations for key stretching

### Security Considerations:
 **Important Notes:**
- Caesar cipher is NOT secure for real data
- Fernet encryption is secure for protecting sensitive files  
- Always keep backups of important files
- Remember your passwords - they cannot be recovered!

### Example Usage:
```bash
 Welcome to the File Encryption/Decryption Tool!

 Choose operation:
1.  Encrypt file
2.  Decrypt file  
3.  Create sample file for testing
Enter your choice (1-3): 3

 Sample file created: sample_text.txt
You can now encrypt/decrypt this file: sample_text.txt
```

## Task 3: N-Queens Problem Solver (`n_queens.py`)

An advanced implementation of the classic N-Queens problem using multiple solving algorithms.

### Features:
- Multiple solving algorithms (recursive, iterative)
- Optimized backtracking with constraint propagation
- Performance benchmarking across different board sizes
- Solution validation and symmetry analysis
- Comprehensive statistics and timing

### How to run:
```bash
python n_queens.py
```

### Solving Methods:
```
 Choose solving method:
1.  Find first solution only (fast)
2.  Find all solutions (slower for large N) 
3.  Iterative approach (first solution)
4.  Performance benchmark
```

### Algorithm Implementations:

#### 1. Basic Backtracking:
```python
def solve_backtrack(self, row: int = 0) -> bool:
    if row >= self.n:
        return True
    
    for col in range(self.n):
        if self.is_safe(row, col):
            self.board[row][col] = 1
            if self.solve_backtrack(row + 1):
                return True
            self.board[row][col] = 0
    return False
```

#### 2. Optimized with Sets:
```python
def solve_all_backtrack(self, row: int = 0, 
                       cols: Set[int] = None,
                       diag1: Set[int] = None, 
                       diag2: Set[int] = None):
    # Uses O(1) conflict detection with sets
    # diag1: row - col, diag2: row + col
```

#### 3. Iterative Implementation:
Uses explicit stack instead of recursion for better memory management.

### Example Solutions:

#### 8-Queens Solution:
```
============================================
            N-QUEENS SOLUTION
============================================
     0   1   2   3   4   5   6   7 
 0   Q   ·       ·       ·       ·  0
 1       ·       ·   Q   ·       ·  1  
 2   ·       ·       ·       ·   Q  2
 3       ·   Q   ·       ·       ·  3
 4   ·       ·       ·       Q   ·  4
 5       Q   ·       ·       ·   ·  5
 6   ·       ·       Q   ·       ·  6
 7       ·       ·       ·   Q   ·  7
     0   1   2   3   4   5   6   7
============================================
```

### Performance Analysis:
```
 PERFORMANCE BENCHMARK:
--------------------------------------------------
N   Solutions  Time (s)   Backtracks
--------------------------------------------------
4   2          0.0012     2            
5   10         0.0034     13             
6   4          0.0089     47           
7   40         0.0234     175          
8   92         0.1156     876          
9   352        0.4523     2847         
```

### Advanced Features:

#### Solution Validation:
```python
def validate_solution(self, solution: List[Tuple[int, int]]) -> bool:
    # Checks for conflicts in rows, columns, and diagonals
    rows, cols, diag1, diag2 = set(), set(), set(), set()
    for row, col in solution:
        if any(conflict_check):
            return False
    return True
```

#### Symmetry Analysis:
For 8×8 board:
- Total solutions: 92
- Fundamental solutions (unique after symmetry): 12
- 8-fold symmetry operations possible

## Getting Started

### Prerequisites:
- Python 3.8 or higher
- Required packages:
  ```bash
  pip install -r requirements.txt
  ```

### Requirements Files:

#### level3/requirements.txt:
```
django>=4.2.0
django-crispy-forms>=2.0
crispy-bootstrap5>=0.7
cryptography>=41.0.0
```

### Running the Tasks:

1. **Django Web App:**
   ```bash
   cd django_auth_app
   python setup_django_project.py
   python manage.py runserver
   ```

2. **File Encryption:**
   ```bash
   pip install cryptography
   python file_encryption.py
   ```

3. **N-Queens Solver:**
   ```bash
   python n_queens.py
   ```

## Learning Objectives

These advanced tasks demonstrate:

### Web Development:
- **Django Framework**: Models, Views, Templates (MVT)
- **Authentication**: User management, sessions, permissions
- **Security**: CSRF, password hashing, secure forms
- **Frontend**: HTML templates, Bootstrap CSS, responsive design

### Cryptography:
- **Symmetric Encryption**: Fernet (AES-128)
- **Key Derivation**: PBKDF2 with salt
- **Security Principles**: Confidentiality, integrity, authentication
- **Practical Security**: Password management, file protection

### Algorithms:
- **Backtracking**: Systematic exploration with pruning
- **Constraint Satisfaction**: N-Queens as CSP problem
- **Optimization**: Set-based conflict detection
- **Analysis**: Time complexity, solution counting

### Software Engineering:
- **Architecture**: MVC pattern, modular design
- **Testing**: Unit tests, validation functions
- **Documentation**: Comprehensive inline documentation
- **Performance**: Benchmarking, profiling, optimization

## Extension Ideas

### Django App:
- Add user roles and permissions
- Implement email verification
- Add two-factor authentication
- Create REST API endpoints
- Add social media authentication

### File Encryption:
- Add asymmetric encryption (RSA)
- Implement digital signatures
- Add file integrity verification
- Create GUI interface
- Add batch encryption capabilities

### N-Queens:
- Implement parallel solving
- Add visualization of solutions
- Extend to N-Rooks, N-Knights problems
- Add genetic algorithm solution
- Create interactive web interface

## Security Best Practices

1. **Never hardcode sensitive information**
2. **Use environment variables for configuration**
3. **Validate all user inputs**
4. **Use secure random number generation**
5. **Implement proper error handling**
6. **Keep dependencies updated**
7. **Follow principle of least privilege**

## Production Deployment

### Django Application:
- Set `DEBUG = False`
- Configure proper database (PostgreSQL)
- Set up static file serving
- Use environment variables for secrets
- Configure HTTPS
- Set up monitoring and logging

These advanced tasks provided me a solid foundation for professional Python development, covering web applications, security, and algorithmic problem-solving.


