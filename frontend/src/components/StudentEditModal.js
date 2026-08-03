import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';

export const StudentEditModal = ({
  student,
  onClose,
  onSave,
  isLoading = false
}) => {
  const [formData, setFormData] = useState({
    prenom: '',
    nom: '',
    email: '',
    phone: '',
    address: '',
    niveau_etude: 'Baccalauréat',
    notes_regionales: '',
    note_generale: '',
    option_bac: 'Maths',
    notes_diplome: '',
    option_diplome: '',
    revenu: '',
    dependants: '',
    distance: '',
    type_sponsorship: 'Complète',
    statut: 'En attente'
  });

  useEffect(() => {
    if (student) {
      // Handle both flat and nested data structures
      const notes_regionales = student.donnees_baccalaureat?.notes_regionales || student.notes_regionales;
      const note_generale = student.donnees_baccalaureat?.note_generale || student.note_generale;
      const option_bac = student.donnees_baccalaureat?.option || student.option_bac || 'Maths';
      const notes_diplome = student.donnees_diplome?.notes_diplome || student.notes_diplome;
      const option_diplome = student.donnees_diplome?.option || student.option_diplome;
      const revenu = student.donnees_financieres?.revenu || student.revenu;
      const dependants = student.donnees_financieres?.dependants || student.dependants;
      const distance = student.donnees_contextuelles?.distance || student.distance;
      
      setFormData({
        prenom: student.prenom || '',
        nom: student.nom || '',
        email: student.email || '',
        phone: student.phone || '',
        address: student.address || '',
        niveau_etude: student.niveau_etude || 'Baccalauréat',
        notes_regionales: notes_regionales ? parseFloat(notes_regionales) : '',
        note_generale: note_generale ? parseFloat(note_generale) : '',
        option_bac: option_bac,
        notes_diplome: notes_diplome ? parseFloat(notes_diplome) : '',
        option_diplome: option_diplome || '',
        revenu: revenu ? parseFloat(revenu) : '',
        dependants: dependants ? parseInt(dependants) : '',
        distance: distance ? parseFloat(distance) : '',
        type_sponsorship: student.type_sponsorship || 'Complète',
        statut: student.statut || 'En attente'
      });
    }
  }, [student]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        {/* Modal Header */}
        <div className="sticky top-0 bg-gradient-to-r from-blue-700 to-blue-800 text-white p-6 border-b border-blue-900 flex justify-between items-center">
          <h2 className="text-2xl font-bold">Modifier: {student?.prenom} {student?.nom}</h2>
          <button
            onClick={onClose}
            disabled={isLoading}
            className="text-blue-100 hover:text-white transition disabled:opacity-50"
          >
            <X size={24} />
          </button>
        </div>

        {/* Modal Content */}
        <form onSubmit={handleSubmit} className="p-6 space-y-6">
          {/* Personal Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Informations Personnelles</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input
                type="text"
                name="prenom"
                placeholder="Prénom *"
                value={formData.prenom}
                onChange={handleChange}
                required
                className="form-input"
              />
              <input
                type="text"
                name="nom"
                placeholder="Nom *"
                value={formData.nom}
                onChange={handleChange}
                required
                className="form-input"
              />
              <input
                type="email"
                name="email"
                placeholder="Email *"
                value={formData.email}
                onChange={handleChange}
                required
                className="form-input"
              />
              <input
                type="tel"
                name="phone"
                placeholder="Téléphone *"
                value={formData.phone}
                onChange={handleChange}
                required
                className="form-input"
              />
              <input
                type="text"
                name="address"
                placeholder="Adresse *"
                value={formData.address}
                onChange={handleChange}
                required
                className="form-input md:col-span-2"
              />
            </div>
          </div>

          {/* Academic Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Informations Académiques</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <select
                name="niveau_etude"
                value={formData.niveau_etude}
                onChange={handleChange}
                className="form-input"
                required
              >
                <option value="Baccalauréat">Baccalauréat</option>
                <option value="Bac+2">Bac+2</option>
                <option value="Bac+3">Bac+3</option>
                <option value="Bac+4">Bac+4</option>
              </select>
              <select
                name="option_bac"
                value={formData.option_bac}
                onChange={handleChange}
                className="form-input"
                required
              >
                <option value="Maths">Maths</option>
                <option value="Physique">Physique</option>
                <option value="SVT">SVT</option>
              </select>
              <input
                type="number"
                step="0.01"
                min="0"
                max="20"
                name="notes_regionales"
                placeholder="Notes Régionales (0-20) *"
                value={formData.notes_regionales}
                onChange={handleChange}
                required
                className="form-input"
              />
              <input
                type="number"
                step="0.01"
                min="0"
                max="20"
                name="note_generale"
                placeholder="Note Générale (0-20) *"
                value={formData.note_generale}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>

            {/* Diploma Fields - Show only for Bac+2 and above */}
            {(formData.niveau_etude === 'Bac+2' || formData.niveau_etude === 'Bac+3' || formData.niveau_etude === 'Bac+4') && (
              <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-3">Informations Diplôme</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    max="20"
                    name="notes_diplome"
                    placeholder="Note Diplôme (0-20) *"
                    required={formData.niveau_etude !== 'Baccalauréat'}
                    value={formData.notes_diplome}
                    onChange={handleChange}
                    className="form-input"
                  />
                  <input
                    type="text"
                    name="option_diplome"
                    placeholder="Spécialité Diplôme (ex: Informatique) *"
                    required={formData.niveau_etude !== 'Baccalauréat'}
                    value={formData.option_diplome}
                    onChange={handleChange}
                    className="form-input"
                  />
                </div>
              </div>
            )}
          </div>

          {/* Financial Information */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Informations Financières</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <input
                type="number"
                name="revenu"
                placeholder="Revenu (DA) *"
                value={formData.revenu}
                onChange={handleChange}
                required
                className="form-input"
              />
              <input
                type="number"
                name="dependants"
                placeholder="Dépendants *"
                min="0"
                value={formData.dependants}
                onChange={handleChange}
                required
                className="form-input"
              />
              <input
                type="number"
                name="distance"
                placeholder="Distance (km) *"
                min="0"
                value={formData.distance}
                onChange={handleChange}
                required
                className="form-input"
              />
            </div>
          </div>

          {/* Sponsorship Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Type de Sponsorship</h3>
              <select
                name="type_sponsorship"
                value={formData.type_sponsorship}
                onChange={handleChange}
                className="form-input"
                required
              >
                <option value="Aucune">Aucune</option>
                <option value="Partielle">Partielle</option>
                <option value="Moitié">Moitié</option>
                <option value="Complète">Complète</option>
              </select>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Statut</h3>
              <select
                name="statut"
                value={formData.statut}
                onChange={handleChange}
                className="form-input"
                required
              >
                <option value="En attente">En attente</option>
                <option value="Approuvé">Approuvé</option>
                <option value="Rejeté">Rejeté</option>
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4 pt-6 border-t border-gray-200">
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 bg-blue-700 hover:bg-blue-800 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition"
            >
              {isLoading ? 'Enregistrement...' : 'Enregistrer les modifications'}
            </button>
            <button
              type="button"
              onClick={onClose}
              disabled={isLoading}
              className="flex-1 bg-gray-600 hover:bg-gray-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition"
            >
              Annuler
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
