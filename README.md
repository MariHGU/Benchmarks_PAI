
# Benchmarks\_PAI

## Getting Started

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Prepare configuration**

   * Set the `TestType` in `main.py` to the desired test type:

     * `PROMPT_ALIGNMENT`
     * `HELPFULNESS`
     * `SUMMARIZATION`
     * `BENCHMARKING`

3. **Run the script**

   ```bash
   python main.py
   ```

---

## Important Notes

* **API Key**
  Before running the script, ensure you have a valid API key stored in a file named `.api_key` located in the **parent directory** of your project.
  This key is required for accessing **OpenWebUI** and **chat.nhn.no** services.

* **Model Configuration**

  * Update `models.csv` with the necessary details for the models you want to test.
  * Make sure each model is **downloaded** and **accessible** through both **OpenWebUI** and **chat.nhn.no**.

---

## Example Workflow

1. Add your `.api_key` file one directory above the project root.
2. Update `models.csv` with model names, IDs, or endpoints.
3. Choose a `TestType` in `main.py`.
4. Run:

   ```bash
   python main.py
   ```
5. View generated responses and evaluation results.