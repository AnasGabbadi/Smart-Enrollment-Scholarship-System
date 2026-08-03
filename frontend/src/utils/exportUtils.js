import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import Papa from 'papaparse';

/**
 * Export a chart canvas as PNG image
 * @param {HTMLElement} chartElement - The chart element to export
 * @param {string} fileName - Name of the file (without extension)
 */
export const exportChartAsImage = async (chartElement, fileName = 'chart') => {
  try {
    const canvas = await html2canvas(chartElement, {
      backgroundColor: '#ffffff',
      scale: 2,
    });
    
    const link = document.createElement('a');
    link.href = canvas.toDataURL('image/png');
    link.download = `${fileName}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    return true;
  } catch (error) {
    console.error('Error exporting chart:', error);
    throw new Error('Erreur lors de l\'export du graphique');
  }
};

/**
 * Export a chart canvas as PDF
 * @param {HTMLElement} chartElement - The chart element to export
 * @param {string} fileName - Name of the file (without extension)
 */
export const exportChartAsPDF = async (chartElement, fileName = 'chart') => {
  try {
    const canvas = await html2canvas(chartElement, {
      backgroundColor: '#ffffff',
      scale: 2,
    });
    
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF({
      orientation: canvas.width > canvas.height ? 'landscape' : 'portrait',
      unit: 'mm',
      format: 'a4'
    });
    
    const pageWidth = pdf.internal.pageSize.getWidth();
    const imgWidth = pageWidth - 20;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    
    pdf.addImage(imgData, 'PNG', 10, 10, imgWidth, imgHeight);
    pdf.save(`${fileName}.pdf`);
    
    return true;
  } catch (error) {
    console.error('Error exporting chart to PDF:', error);
    throw new Error('Erreur lors de l\'export en PDF');
  }
};

/**
 * Export data as CSV
 * @param {Array} data - Array of objects to export
 * @param {string} fileName - Name of the file (without extension)
 */
export const exportDataAsCSV = (data, fileName = 'data') => {
  try {
    const csv = Papa.unparse(data, {
      quotes: true,
      quoteChar: '"',
      header: true,
      encoding: 'utf-8'
    });
    
    const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `${fileName}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    return true;
  } catch (error) {
    console.error('Error exporting data:', error);
    throw new Error('Erreur lors de l\'export des données');
  }
};

/**
 * Export students data with formatted fields
 * @param {Array} students - Array of student objects
 * @param {string} fileName - Name of the file
 */
export const exportStudentsAsCSV = (students, fileName = 'etudiants') => {
  try {
    const formattedData = students.map(student => ({
      'Prénom': student.prenom || '',
      'Nom': student.nom || '',
      'Email': student.email || '',
      'GPA': parseFloat(student.gpa) || '',
      'Notes Examen': parseFloat(student.notes_examen) || '',
      'Revenu': parseFloat(student.revenu) || '',
      'Dépendants': student.dependants || '',
      'Distance (km)': student.distance || '',
      'Type Bourse': student.type_bourse || '',
      'Montant Bourse': parseFloat(student.montant_bourse) || '',
      'Statut': student.statut || '',
      'Date Inscription': student.date_inscription || '',
    }));
    
    return exportDataAsCSV(formattedData, fileName);
  } catch (error) {
    console.error('Error exporting students:', error);
    throw new Error('Erreur lors de l\'export des étudiants');
  }
};

/**
 * Export statistics summary as CSV
 * @param {Object} stats - Statistics object
 * @param {string} fileName - Name of the file
 */
export const exportStatisticsAsCSV = (stats, fileName = 'statistiques') => {
  try {
    const statsArray = [
      { 'Métrique': 'Total Étudiants', 'Valeur': stats.totalStudents || 0 },
      { 'Métrique': 'Approuvés', 'Valeur': stats.approved || 0 },
      { 'Métrique': 'En Attente', 'Valeur': stats.pending || 0 },
      { 'Métrique': 'Rejetés', 'Valeur': stats.rejected || 0 },
      { 'Métrique': 'GPA Moyen', 'Valeur': (stats.avgGPA || 0).toFixed(2) },
      { 'Métrique': 'Total Bourses', 'Valeur': (stats.totalScholarship || 0).toFixed(2) },
    ];
    
    return exportDataAsCSV(statsArray, fileName);
  } catch (error) {
    console.error('Error exporting statistics:', error);
    throw new Error('Erreur lors de l\'export des statistiques');
  }
};
