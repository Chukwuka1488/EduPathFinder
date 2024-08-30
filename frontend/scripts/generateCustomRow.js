// frontend/scripts/generateCustomRow.js

/**
 * Generates a custom row's HTML content
 * @returns {string} - The HTML content for the custom row
 */
function generateCustomRow() {
  return `
      <th class="border p-2 font-normal text-white border-transparent" style="font-size: 10px"></th>
      <th class="border p-2 font-normal text-white border-transparent" style="font-size: 10px"></th>
      <th class="border p-2 font-normal important text-white border-transparent" style="font-size: 10px" data-key="important">!</th>
      <th class="border p-2 font-normal hours text-white border-transparent" style="font-size: 10px" data-key="hours">H</th>
      <th class="border p-2 font-normal course-code text-white border-transparent" style="font-size: 10px"data-key="course_number">Course #</th>
      <th class="border p-2 font-normal course-title text-white border-transparent" style="font-size: 10px" data-key="title">Course Title</th>
      <th class="border p-2 font-normal min-grade text-white border-transparent" style="font-size: 10px" data-key="min_grade">Min. Grade</th>
      <th class="border p-2 font-normal gec text-white border-transparent" style="font-size: 10px" data-key="gec">GEC</th>
      <th class="border p-2 font-normal prereq text-white border-transparent" style="font-size: 10px" data-key="prerequisite">Prerequisite</th>
      <th class="border p-2 font-normal add-notes text-white border-transparent" style="font-size: 10px" data-key="additional_notes">Additional Notes</th>
    `;
}

export { generateCustomRow };
