import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { LogIn, AlertCircle, Eye, EyeOff, Lock } from 'lucide-react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

const Login = ({ onLogin }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('admin@admin.com');
  const [password, setPassword] = useState('adminpassword');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // For demo purposes, accept hardcoded admin credentials
      if (email === 'admin@admin.com' && password === 'adminpassword') {
        const token = 'admin-token-' + Date.now();
        onLogin(token, 'admin', { email, name: 'Admin User', role: 'admin' });
        navigate('/admin/dashboard');
      } else {
        setError('Identifiants invalides. Veuillez utiliser les identifiants administrateur corrects.');
      }
    } catch (err) {
      setError('Échec de la connexion. Veuillez réessayer.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-900 via-blue-900 to-blue-800">
      <Navbar isAuthenticated={false} userRole={null} onLogout={() => {}} />

      <div className="flex-1 flex items-center justify-center px-4 py-12 relative">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <svg className="w-full h-full" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="admin-zelij" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
                <rect width="40" height="40" fill="white" opacity="0.05"/>
                <path d="M20,0 L40,20 L20,40 L0,20 Z" stroke="white" strokeWidth="1" fill="none" opacity="0.3"/>
              </pattern>
            </defs>
            <rect width="200" height="200" fill="url(#admin-zelij)"/>
          </svg>
        </div>

        <div className="w-full max-w-md relative z-10">
          {/* Login Card - Moroccan Admin Style */}
          <div className="bg-white rounded-2xl shadow-2xl overflow-hidden border-t-4 border-amber-600">
            {/* Decorative Header */}
            <div className="bg-gradient-to-r from-slate-900 via-blue-900 to-blue-800 text-white p-8 text-center relative overflow-hidden">
              <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-amber-500 via-red-500 to-amber-500"></div>
              
              {/* Admin Badge */}
              <div className="inline-block bg-gradient-to-br from-amber-500 to-orange-500 text-white p-4 rounded-full mb-4 border-4 border-white border-opacity-30 shadow-lg">
                <Lock size={32} />
              </div>
              <h1 className="text-3xl font-bold mb-2">Portail Administrateur</h1>
              <p className="text-blue-100 text-sm font-medium">Accès sécurisé au système de gestion des bourses</p>
            </div>

            {/* Form Container */}
            <div className="p-8">
              {/* Error Message */}
              {error && (
                <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-600 rounded flex items-start space-x-3">
                  <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
                  <p className="text-red-700 text-sm font-medium">{error}</p>
                </div>
              )}

              {/* Form */}
              <form onSubmit={handleLogin} className="space-y-6">
                {/* Email Field */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">🔑 Email Administrateur</label>
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-600 focus:bg-blue-50 transition"
                    placeholder="admin@admin.com"
                    required
                  />
                </div>

                {/* Password Field */}
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">🔐 Mot de passe</label>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-600 focus:bg-blue-50 transition pr-12"
                      placeholder="••••••••"
                      required
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-3 text-gray-600 hover:text-blue-600"
                    >
                      {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                    </button>
                  </div>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3 bg-gradient-to-r from-blue-700 to-blue-600 text-white font-bold rounded-lg hover:from-blue-800 hover:to-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 duration-200 shadow-md flex items-center justify-center space-x-2"
                >
                  <LogIn size={20} />
                  <span>{loading ? '⏳ Connexion en cours...' : '🚀 Accéder au Tableau de Bord'}</span>
                </button>
              </form>

              {/* Divider */}
              <div className="my-6 flex items-center">
                <div className="flex-1 border-t border-gray-300"></div>
                <div className="px-3 text-gray-500 text-sm">Identifiants Démo</div>
                <div className="flex-1 border-t border-gray-300"></div>
              </div>

              {/* Demo Credentials Card */}
              <div className="p-4 bg-gradient-to-br from-blue-50 to-amber-50 border border-blue-200 rounded-lg">
                <p className="text-sm font-bold text-blue-900 mb-3 flex items-center space-x-2">
                  <span>📋 Identifiants de Démonstration:</span>
                </p>
                <div className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-gray-600 text-sm">Email:</span>
                    <code className="bg-white px-3 py-1 rounded border border-blue-200 text-blue-700 font-mono text-sm">admin@admin.com</code>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-gray-600 text-sm">Mot de passe:</span>
                    <code className="bg-white px-3 py-1 rounded border border-blue-200 text-blue-700 font-mono text-sm">adminpassword</code>
                  </div>
                </div>
              </div>
            </div>

            {/* Footer Link */}
            <div className="bg-gradient-to-r from-gray-50 to-blue-50 px-8 py-6 border-t border-gray-200 text-center">
              <p className="text-gray-700 text-sm">
                Pas administrateur?{' '}
                <Link to="/" className="font-bold text-blue-600 hover:text-blue-700 underline">
                  Aller à l'accueil
                </Link>
              </p>
              <p className="text-gray-500 text-xs mt-2">
                Accès sécurisé - Session limitée à 8 heures
              </p>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Login;
