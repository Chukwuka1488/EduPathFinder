// frontend/scripts/addCoreGECInfo.js

function addCoreGECInfo(tableBody) {
  // Line 1 - Core course catalog link
  const coreCatalogRow = document.createElement("tr");
  coreCatalogRow.innerHTML = `
      <td colspan="10" class="text-center font-bold" style="border: 1px solid #f4f9fb; font-size: 9px;">
        CORE: The 2024-2026 list of core courses can be found in the 2024-2026 Undergraduate Catalog: <a href="www.utrgv.edu/catalog" target="_blank">www.utrgv.edu/catalog</a> > See 'Core Curriculum'
      </td>
    `;
  tableBody.appendChild(coreCatalogRow);

  // Line 2 - Symbols Key
  const symbolsKeyRow = document.createElement("tr");
  symbolsKeyRow.innerHTML = `
      <td colspan="10" class="text-left font-bold" style="border: 1px solid #f4f9fb; font-size: 9px;">
        Symbols Key
      </td>
    `;
  tableBody.appendChild(symbolsKeyRow);

  // Line 3 - Minimum Grade and GEC Sections Part 1
  const gradesAndGECA = document.createElement("tr");
  gradesAndGECA.innerHTML = `
      <td colspan="8" class="text-left" style="border: 1px solid #f4f9fb; font-size: 9px;">
        <strong>Minimum Grade:</strong> A - Excellent; B - Good; C - Satisfactory; D - Below Average; CR - Credit; P - Passing; S - Satisfactory.
      </td>
      <td colspan="2" class="text-right" style="border: 1px solid #f4f9fb; font-size: 9px;">
        <strong>General Education Core (GEC) Sections:</strong> 010 - Communication; 020 - Mathematics; 030 - Life and Physical Sciences; 040 - Language, Philosophy & Culture;
      </td>
    `;
  tableBody.appendChild(gradesAndGECA);

  // Line 4 - Program Admission Requirement and GEC Sections Part 2
  const programAdmissionAndGECB = document.createElement("tr");
  programAdmissionAndGECB.innerHTML = `
      <td colspan="7" class="text-left" style="border: 1px solid #f4f9fb; font-size: 9px;">
        <strong>Bolded Course #:</strong> Program Admission Requirement
      </td>
      <td colspan="3" class="text-right" style="border: 1px solid #f4f9fb; font-size: 9px;">
        050 - Creative Arts; 060 - American History; 070 - Government/Political Science; 080 - Social and Behavioral Sciences; 090 - Applied Communication and Literacies;
      </td>
    `;
  tableBody.appendChild(programAdmissionAndGECB);

  // Line 5 - GEC Sections Part 3
  const gecPartCRow = document.createElement("tr");
  gecPartCRow.innerHTML = `
      <td colspan="10" class="text-right" style="border: 1px solid #f4f9fb; font-size: 9px;">
        090 - Humanities; 090 - Leadership; 090 - Science Labs; 090 - Interdisciplinary; 090 - Technologies; 090 - Language Diversity & Writing.
      </td>
    `;
  tableBody.appendChild(gecPartCRow);
}

export { addCoreGECInfo };
