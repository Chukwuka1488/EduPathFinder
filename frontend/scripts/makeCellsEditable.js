// frontend/scripts/makeCellsEditable.js
import { updateCourseData } from "./updateCourseData.js";

/**
 * Make table cells editable
 */
function makeCellsEditable() {
  document.querySelectorAll(".data-table td").forEach((cell) => {
    // Skip if it's a header or a non-editable column
    if (cell.querySelector("input") || cell.dataset.editable === "false")
      return;

    cell.addEventListener("click", function () {
      if (this.querySelector("input")) return;

      const currentText = this.innerText.trim();
      console.log(`Editing cell with initial value: ${currentText}`);

      const input = document.createElement("input");
      input.type = "text";
      input.value = currentText;
      input.className =
        "w-full p-1 border border-gray-300 rounded focus:outline-none focus:border-blue-500";
      this.innerHTML = "";
      this.appendChild(input);
      input.focus();

      const finalizeUpdate = () => {
        const newValue = input.value.trim() || currentText;
        cell.innerHTML = newValue;
        console.log(`Cell value updated to: ${newValue}`);
        updateCourseData(cell, newValue); // Call update function when editing is done
        console.log(`Finalized update for cell: ${newValue}`);
      };

      input.addEventListener("blur", function () {
        console.log("Input blurred, finalizing update...");
        finalizeUpdate();
      });

      input.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
          console.log("Enter key pressed, finalizing update...");
          finalizeUpdate();
        }
      });
    });
  });
}

export { makeCellsEditable };
