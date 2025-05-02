**Prerequisites:**

*   Python 3.11 installed and added to PATH.
*   `pip` (Python package installer).

**Steps:**

1.  **Clone the Repository (Optional):**
    ```bash
    git clone <your-repository-url>
    cd <repository-folder-name>/online_banking
    ```
    *Replace `<repository-folder-name>` with the actual folder name, often `online_banking` if cloned that way, or the parent folder if you cloned the repo containing `online_banking`.*
    *If you downloaded the code directly, navigate to the `online_banking` directory containing `manage.py`.*

2.  **Create and Activate Virtual Environment:**
    *   Navigate to the directory *containing* the `online_banking` folder (e.g., `cd ..` if you are inside `online_banking`).
    *   Create the environment:
        ```bash
        python -m venv venv
        ```
    *   Activate the environment:
        *   Windows: `venv\Scripts\activate`
        *   macOS/Linux: `source venv/bin/activate`

3.  **Install Dependencies:**
    *   Navigate *into* the `online_banking` directory (where `requirements.txt` and `manage.py` are).
        ```bash
        cd online_banking
        ```
    *   Install required packages:
        ```bash
        # If you encounter SSL errors (often on corporate networks), try adding --trusted-host flags:
        # pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
        pip install -r requirements.txt
        ```
        *(If installation fails requiring C++ build tools, follow instructions to install "Desktop development with C++" from the Visual Studio Installer, restart, activate venv, and try `pip install` again).*

4.  **Place Dataset:**
    *   Ensure the dataset file `loan_amount_prediction_dataset_v2.csv` is present in the project root directory (`online_banking/`).

5.  **Train the ML Model:**
    *   Run the training script. This will create the `ml_model/loan_pipeline.pkl` file. **This step may take several minutes** due to GridSearchCV.
    ```bash
    python ml_model/train_model.py
    ```

6.  **Apply Database Migrations:**
    *   Create and apply database schema changes.
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

8.  **Access the Application:**
    *   Open your web browser and go to `http://127.0.0.1:8000/`. You should be redirected to the login page.

## Running Tests

1.  Ensure your virtual environment is activated.
2.  Navigate to the project root directory (`online_banking/`).
3.  Run the test suite:
    ```bash
    python manage.py test
    ```
    *   To run tests for a specific app:
        ```bash
        python manage.py test banking # Example for banking app
        ```

---
