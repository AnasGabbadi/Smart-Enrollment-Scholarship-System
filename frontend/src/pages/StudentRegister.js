import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserPlus, AlertCircle, CheckCircle } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import studentService from '../services/studentService';

const StudentRegister = ({ onLogin }) => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    // Personal Info
    prenom: '',
    nom: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
    address: '',
    annee: new Date().getFullYear(),
    
    // Education Level
    niveau_etude: 'Baccalauréat', // 'Baccalauréat' | 'Bac+2' | 'Bac+3' | 'Bac+4'
    
    // Baccalauréat Data
    notes_regionales: '',
    note_generale: '',
    option_bac: 'Maths', // 'Maths' | 'Physique' | 'SVT'
    
    // Diplôme Data (for Bac+2 and above)
    notes_diplome: '',
    option_diplome: '',
    
    // Financial & Context
    revenu: '',
    dependants: '',
    distance: '',
    
    // Sponsorship Type
    type_sponsorship: 'Complète', // 'Complète' | 'Partielle' | 'Moitié'
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1);
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateStep1 = () => {
    const newErrors = {};
    if (!formData.prenom.trim()) newErrors.prenom = 'Le prénom est requis';
    if (!formData.nom.trim()) newErrors.nom = 'Le nom est requis';
    if (!formData.email.includes('@')) newErrors.email = 'Un email valide est requis';
    if (formData.password.length < 6) newErrors.password = 'Le mot de passe doit contenir au moins 6 caractères';
    if (formData.password !== formData.confirmPassword) newErrors.confirmPassword = 'Les mots de passe ne correspondent pas';
    if (!formData.phone.trim()) newErrors.phone = 'Le numéro de téléphone est requis';
    if (!formData.address.trim()) newErrors.address = 'L\'adresse est requise';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validateStep2 = () => {
    const newErrors = {};
    
    // Validate Baccalauréat data
    if (!formData.notes_regionales || parseFloat(formData.notes_regionales) < 0 || parseFloat(formData.notes_regionales) > 20) {
      newErrors.notes_regionales = 'Les notes régionales doivent être entre 0 et 20';
    }
    if (!formData.note_generale || parseFloat(formData.note_generale) < 0 || parseFloat(formData.note_generale) > 20) {
      newErrors.note_generale = 'La note générale doit être entre 0 et 20';
    }
    
    // Validate Diplôme data if Bac+2 or above
    if (['Bac+2', 'Bac+3', 'Bac+4'].includes(formData.niveau_etude)) {
      if (!formData.notes_diplome || parseFloat(formData.notes_diplome) < 0 || parseFloat(formData.notes_diplome) > 20) {
        newErrors.notes_diplome = 'Les notes du diplôme doivent être entre 0 et 20';
      }
      if (!formData.option_diplome.trim()) {
        newErrors.option_diplome = 'La spécialité du diplôme est requise';
      }
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validateStep3 = () => {
    const newErrors = {};
    if (!formData.revenu || parseFloat(formData.revenu) < 0) {
      newErrors.revenu = 'Le revenu familial doit être un nombre positif';
    }
    if (!formData.dependants || parseInt(formData.dependants) < 0) {
      newErrors.dependants = 'Le nombre de dépendants doit être 0 ou positif';
    }
    if (!formData.distance || parseFloat(formData.distance) < 0) {
      newErrors.distance = 'La distance doit être un nombre positif';
    }
    if (!formData.type_sponsorship) {
      newErrors.type_sponsorship = 'Veuillez sélectionner un type de parrainage';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (step === 1 && validateStep1()) {
      setStep(2);
    } else if (step === 2 && validateStep2()) {
      setStep(3);
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
      setErrors({});
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateStep3()) return;

    setLoading(true);
    setErrors({});
    
    try {
      // Prepare data in the format expected by backend
      const registrationData = {
        prenom: formData.prenom,
        nom: formData.nom,
        email: formData.email,
        password: formData.password,
        phone: formData.phone,
        address: formData.address,
        annee: formData.annee,
        niveau_etude: formData.niveau_etude,
        donnees_baccalaureat: {
          notes_regionales: parseFloat(formData.notes_regionales),
          note_generale: parseFloat(formData.note_generale),
          option: formData.option_bac
        },
        donnees_diplome: ['Bac+2', 'Bac+3', 'Bac+4'].includes(formData.niveau_etude) ? {
          notes_diplome: parseFloat(formData.notes_diplome),
          option: formData.option_diplome
        } : null,
        donnees_financieres: {
          revenu: parseFloat(formData.revenu),
          dependants: parseInt(formData.dependants)
        },
        donnees_contextuelles: {
          distance: parseFloat(formData.distance)
        },
        type_sponsorship: formData.type_sponsorship
      };
      
      // Call backend to register student
      const response = await studentService.registerStudent(registrationData);
      
      // Success - store student data
      localStorage.setItem('studentData', JSON.stringify(response));
      localStorage.setItem('studentEmail', formData.email);
      
      setSuccess(true);
      
      // Redirect to login after 3 seconds
      setTimeout(() => {
        navigate('/student/login');
      }, 3000);
      
    } catch (err) {
      console.error('Erreur d\'enregistrement:', err);
      
      // Handle Pydantic validation errors (422 responses)
      if (err.response?.status === 422 && Array.isArray(err.response?.data?.detail)) {
        const validationErrors = err.response.data.detail;
        const errorMessages = validationErrors
          .map(error => {
            const field = error.loc?.[1] || error.loc?.[0] || 'unknown';
            const message = error.msg || 'Erreur de validation';
            return `${field}: ${message}`;
          })
          .join('\n');
        setErrors({ submit: errorMessages });
      } else {
        // Handle other error types
        const errorMessage = err.response?.data?.detail || 'L\'enregistrement a échoué. Veuillez réessayer.';
        setErrors({ submit: typeof errorMessage === 'string' ? errorMessage : JSON.stringify(errorMessage) });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-slate-50 to-blue-50">
      <Navbar isAuthenticated={false} userRole={null} onLogout={() => {}} />

      <div className="flex-1 flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-2xl">
          {/* Registration Card - Moroccan Style */}
          <div className="bg-white rounded-2xl shadow-2xl overflow-hidden border-t-4 border-blue-600">
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-500 text-white p-8 text-center relative">
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-amber-500 via-red-500 to-amber-500"></div>
              <div className="inline-block bg-white bg-opacity-20 text-white p-4 rounded-full mb-4 border-2 border-white border-opacity-30">
                <UserPlus size={32} />
              </div>
              <h1 className="text-3xl font-bold mb-2">Formulaire d'Inscription</h1>
              <p className="text-blue-100">Candidatez pour notre programme de bourses d'excellence</p>
            </div>

            {/* Content Container */}
            <div className="p-8">
              {/* Progress Bar - Moroccan Style */}
              <div className="mb-8">
                <div className="flex items-center space-x-4 mb-4">
                  <div className={`h-12 w-12 rounded-full flex items-center justify-center font-bold text-white ${step >= 1 ? 'bg-gradient-to-br from-blue-600 to-blue-500' : 'bg-gray-300'}`}>
                    1
                  </div>
                  <div className={`flex-1 h-1 rounded ${step >= 2 ? 'bg-gradient-to-r from-blue-600 to-blue-400' : 'bg-gray-300'}`}></div>
                  <div className={`h-12 w-12 rounded-full flex items-center justify-center font-bold text-white ${step >= 2 ? 'bg-gradient-to-br from-blue-600 to-blue-500' : 'bg-gray-300'}`}>
                    2
                  </div>
                  <div className={`flex-1 h-1 rounded ${step >= 3 ? 'bg-gradient-to-r from-blue-600 to-blue-400' : 'bg-gray-300'}`}></div>
                  <div className={`h-12 w-12 rounded-full flex items-center justify-center font-bold text-white ${step >= 3 ? 'bg-gradient-to-br from-blue-600 to-blue-500' : 'bg-gray-300'}`}>
                    3
                  </div>
                </div>
                <div className="text-center text-sm font-semibold text-blue-600">
                  <span>{Math.round((step / 3) * 100)}% Complété</span>
                </div>
              </div>

              {/* Step Labels */}
              <div className="mb-8 text-center p-4 bg-gradient-to-r from-blue-50 to-amber-50 rounded-lg border border-blue-200">
                {step === 1 && <p className="text-lg font-bold text-blue-900">📝 Étape 1: Informations Personnelles</p>}
                {step === 2 && <p className="text-lg font-bold text-blue-900">🎓 Étape 2: Données Académiques</p>}
                {step === 3 && <p className="text-lg font-bold text-blue-900">💰 Étape 3: Informations Financières</p>}
              </div>

              {/* Error Message */}
              {errors.submit && (
                <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-600 rounded">
                  <div className="flex items-start space-x-3">
                    <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
                    <div className="flex-1">
                      {errors.submit.split('\n').map((line, idx) => (
                        <p key={idx} className="text-red-700 text-sm mb-1">{line}</p>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* Success Message */}
              {success && (
                <div className="mb-6 p-4 bg-green-50 border-l-4 border-green-600 rounded flex items-start space-x-3">
                  <CheckCircle className="text-green-600 flex-shrink-0 mt-0.5" size={20} />
                  <div>
                    <p className="text-green-700 font-semibold">✅ Inscription réussie!</p>
                    <p className="text-green-600 text-sm mt-1">Votre demande a été soumise avec succès. Vous serez redirigé vers la page de connexion...</p>
                  </div>
                </div>
              )}

              {/* Step 1: Personal Information */}
              {step === 1 && !success && (
                <form className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="form-label">Prénom *</label>
                    <input
                      type="text"
                      name="prenom"
                      value={formData.prenom}
                      onChange={handleChange}
                      className="form-input"
                      placeholder="Jean"
                    />
                    {errors.prenom && <p className="text-red-600 text-sm mt-1">{errors.prenom}</p>}
                  </div>

                  <div>
                    <label className="form-label">Nom de Famille *</label>
                    <input
                      type="text"
                      name="nom"
                      value={formData.nom}
                      onChange={handleChange}
                      className="form-input"
                      placeholder="Dupont"
                    />
                    {errors.nom && <p className="text-red-600 text-sm mt-1">{errors.nom}</p>}
                  </div>

                  <div>
                    <label className="form-label">Adresse E-mail *</label>
                    <input
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      className="form-input"
                      placeholder="jean@example.com"
                    />
                    {errors.email && <p className="text-red-600 text-sm mt-1">{errors.email}</p>}
                  </div>

                  <div>
                    <label className="form-label">Numéro de Téléphone *</label>
                    <input
                      type="tel"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      className="form-input"
                      placeholder="+33 1 23 45 67 89"
                    />
                    {errors.phone && <p className="text-red-600 text-sm mt-1">{errors.phone}</p>}
                  </div>

                  <div>
                    <label className="form-label">Adresse *</label>
                    <input
                      type="text"
                      name="address"
                      value={formData.address}
                      onChange={handleChange}
                      className="form-input"
                      placeholder="123 Main Street"
                    />
                    {errors.address && <p className="text-red-600 text-sm mt-1">{errors.address}</p>}
                  </div>

                  <div>
                    <label className="form-label">City *</label>
                    <input
                      type="text"
                      name="city"
                      value={formData.city}
                      onChange={handleChange}
                      className="form-input"
                      placeholder="New York"
                    />
                  </div>

                  <div>
                    <label className="form-label">Password *</label>
                    <input
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      className="form-input"
                      placeholder="••••••••"
                    />
                    {errors.password && <p className="text-red-600 text-sm mt-1">{errors.password}</p>}
                  </div>

                  <div>
                    <label className="form-label">Confirm Password *</label>
                    <input
                      type="password"
                      name="confirmPassword"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      className="form-input"
                      placeholder="••••••••"
                    />
                    {errors.confirmPassword && <p className="text-red-600 text-sm mt-1">{errors.confirmPassword}</p>}
                  </div>
                </div>

                <button
                  type="button"
                  onClick={handleNext}
                  className="btn-primary w-full"
                >
                  Continue to Academic & Financial Info
                </button>
              </form>
            )}

            {/* Step 2: Academic Information (Moroccan System) */}
            {step === 2 && !success && (
              <form className="space-y-6">
                <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
                  <p className="text-blue-900 text-sm">
                    Remplissez vos informations académiques selon le système marocain. Les notes doivent être entre 0 et 20.
                  </p>
                </div>

                {/* Education Level Selection */}
                <div>
                  <label className="form-label">Niveau d'Études *</label>
                  <select
                    name="niveau_etude"
                    value={formData.niveau_etude}
                    onChange={handleChange}
                    className="form-input"
                  >
                    <option value="Baccalauréat">Baccalauréat (Lycée)</option>
                    <option value="Bac+2">Bac+2 (Diplôme)</option>
                    <option value="Bac+3">Bac+3</option>
                    <option value="Bac+4">Bac+4</option>
                  </select>
                </div>

                {/* Baccalauréat Section */}
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Données du Baccalauréat</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="form-label">Notes Régionales (0-20) *</label>
                      <input
                        type="number"
                        name="notes_regionales"
                        value={formData.notes_regionales}
                        onChange={handleChange}
                        step="0.01"
                        min="0"
                        max="20"
                        className="form-input"
                        placeholder="16.5"
                      />
                      {errors.notes_regionales && <p className="text-red-600 text-sm mt-1">{errors.notes_regionales}</p>}
                    </div>

                    <div>
                      <label className="form-label">Note Générale (0-20) *</label>
                      <input
                        type="number"
                        name="note_generale"
                        value={formData.note_generale}
                        onChange={handleChange}
                        step="0.01"
                        min="0"
                        max="20"
                        className="form-input"
                        placeholder="17.0"
                      />
                      {errors.note_generale && <p className="text-red-600 text-sm mt-1">{errors.note_generale}</p>}
                    </div>

                    <div className="md:col-span-2">
                      <label className="form-label">Option du Bac *</label>
                      <select
                        name="option_bac"
                        value={formData.option_bac}
                        onChange={handleChange}
                        className="form-input"
                      >
                        <option value="Maths">Mathématiques</option>
                        <option value="Physique">Physiques et Chimie</option>
                        <option value="SVT">Sciences de la Vie et de la Terre</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* Diplôme Section (for Bac+2 and above) */}
                {['Bac+2', 'Bac+3', 'Bac+4'].includes(formData.niveau_etude) && (
                  <div className="bg-gray-50 p-6 rounded-lg">
                    <h3 className="text-lg font-bold text-gray-900 mb-4">Données du Diplôme</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="form-label">Notes du Diplôme (0-20) *</label>
                        <input
                          type="number"
                          name="notes_diplome"
                          value={formData.notes_diplome}
                          onChange={handleChange}
                          step="0.01"
                          min="0"
                          max="20"
                          className="form-input"
                          placeholder="15.5"
                        />
                        {errors.notes_diplome && <p className="text-red-600 text-sm mt-1">{errors.notes_diplome}</p>}
                      </div>

                      <div>
                        <label className="form-label">Spécialité du Diplôme *</label>
                        <input
                          type="text"
                          name="option_diplome"
                          value={formData.option_diplome}
                          onChange={handleChange}
                          className="form-input"
                          placeholder="Informatique, Commerce, etc."
                        />
                        {errors.option_diplome && <p className="text-red-600 text-sm mt-1">{errors.option_diplome}</p>}
                      </div>
                    </div>
                  </div>
                )}

                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={handleBack}
                    className="btn-secondary flex-1"
                  >
                    Retour
                  </button>
                  <button
                    type="button"
                    onClick={handleNext}
                    className="btn-primary flex-1"
                  >
                    Suivant
                  </button>
                </div>
              </form>
            )}

            {/* Step 3: Financial Information */}
            {step === 3 && !success && (
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
                  <p className="text-blue-900 text-sm">
                    Veuillez vous assurer que toutes les informations sont exactes. Fournir de fausses informations peut entraîner une disqualification. Après vérification, l'administration de l'école vous contactera pour demander les documents originaux.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="form-label">Revenu Familial Annuel *</label>
                    <input
                      type="number"
                      name="revenu"
                      value={formData.revenu}
                      onChange={handleChange}
                      className="form-input"
                      placeholder="25000"
                    />
                    {errors.revenu && <p className="text-red-600 text-sm mt-1">{errors.revenu}</p>}
                  </div>

                  <div>
                    <label className="form-label">Nombre de Dépendants *</label>
                    <input
                      type="number"
                      name="dependants"
                      value={formData.dependants}
                      onChange={handleChange}
                      min="0"
                      className="form-input"
                      placeholder="3"
                    />
                    {errors.dependants && <p className="text-red-600 text-sm mt-1">{errors.dependants}</p>}
                  </div>

                  <div>
                    <label className="form-label">Distance de l'Université (km) *</label>
                    <input
                      type="number"
                      name="distance"
                      value={formData.distance}
                      onChange={handleChange}
                      step="0.1"
                      className="form-input"
                      placeholder="50"
                    />
                    {errors.distance && <p className="text-red-600 text-sm mt-1">{errors.distance}</p>}
                  </div>

                  <div>
                    <label className="form-label">Type de Parrainage *</label>
                    <select
                      name="type_sponsorship"
                      value={formData.type_sponsorship}
                      onChange={handleChange}
                      className="form-input"
                    >
                      <option value="Complète">Complète (100%)</option>
                      <option value="Partielle">Partielle (Partielle)</option>
                      <option value="Moitié">Moitié (50%)</option>
                    </select>
                    {errors.type_sponsorship && <p className="text-red-600 text-sm mt-1">{errors.type_sponsorship}</p>}
                  </div>

                  <div>
                    <label className="form-label">Année d'Inscription</label>
                    <input
                      type="number"
                      name="annee"
                      value={formData.annee}
                      onChange={handleChange}
                      className="form-input"
                    />
                  </div>
                </div>

                <div className="flex space-x-4">
                  <button
                    type="button"
                    onClick={handleBack}
                    className="btn-secondary flex-1"
                  >
                    Retour
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? 'Enregistrement en cours...' : 'Terminer l\'inscription'}
                  </button>
                </div>
                </form>
            )}

            {/* Link to Login */}
            <div className="mt-6 text-center text-gray-600 text-sm">
              <p>Vous avez déjà un compte? <Link to="/student-login" className="text-blue-600 hover:underline">Connectez-vous ici</Link></p>
            </div>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default StudentRegister;
