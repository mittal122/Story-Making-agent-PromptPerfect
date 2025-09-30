
import { useState } from 'react';
import './App.css';

function App() {
  const [mode, setMode] = useState('humanize');
  const [formData, setFormData] = useState({
    raw_script: '',
    topic: '',
    genre: 'mysterious',
    description: '',
    duration_seconds: 45,
    api_key: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleModeChange = (newMode) => {
    setMode(newMode);
    setError('');
    setResult(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const payload = {
        mode,
        ...formData,
        duration_seconds: parseInt(formData.duration_seconds)
      };

      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'An error occurred');
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="container">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <a className="navbar-brand" href="#">
          <i className="fas fa-video me-2"></i>
          Hindi Script Generator
        </a>
        <div className="navbar-nav ms-auto">
          <button className="btn btn-outline-warning btn-sm" data-bs-toggle="modal" data-bs-target="#apiModal">
            <i className="fas fa-key me-1"></i>
            API Settings
          </button>
        </div>
      </nav>

      <div className="row">
        <div className="col-lg-6">
          <div className="card shadow-lg border-0">
            <div className="card-header bg-gradient border-0">
              <h5 className="card-title mb-0 text-light">
                <i className="fas fa-pen-fancy me-2 text-warning"></i>
                Script Generator
              </h5>
              <small className="text-light opacity-75">Powered by AI for YouTube Algorithm Optimization</small>
            </div>
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                {/* Mode Selection */}
                <div className="mb-4">
                  <label className="form-label fw-bold">
                    <i className="fas fa-cog me-2 text-primary"></i>
                    Script Mode
                  </label>
                  <div className="row g-3">
                    <div className="col-md-6">
                      <div className={`card border-2 ${mode === 'humanize' ? 'border-warning bg-warning bg-opacity-10' : 'border-light'}`} 
                           onClick={() => handleModeChange('humanize')}>
                        <div className="card-body text-center p-3 cursor-pointer">
                          <i className="fas fa-magic fa-2x text-warning mb-2"></i>
                          <h6 className="fw-bold">Mode 1: Humanize</h6>
                          <small className="text-muted">Transform existing script into engaging, human-like narration</small>
                        </div>
                      </div>
                    </div>
                    <div className="col-md-6">
                      <div className={`card border-2 ${mode === 'generate' ? 'border-success bg-success bg-opacity-10' : 'border-light'}`}
                           onClick={() => handleModeChange('generate')}>
                        <div className="card-body text-center p-3 cursor-pointer">
                          <i className="fas fa-pen-nib fa-2x text-success mb-2"></i>
                          <h6 className="fw-bold">Mode 2: Generate</h6>
                          <small className="text-muted">Create new script from topic and genre with storytelling</small>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Mode 1: Humanize Script Input */}
                {mode === 'humanize' && (
                  <div className="mb-3">
                    <label htmlFor="raw_script" className="form-label">
                      <i className="fas fa-file-text me-1 text-warning"></i>
                      Existing Script to Humanize *
                    </label>
                    <textarea 
                      className="form-control" 
                      name="raw_script" 
                      rows="8"
                      value={formData.raw_script}
                      onChange={handleInputChange}
                      placeholder="Paste your existing script here...

• The AI will rewrite it in a human, engaging, storytelling style
• Maintains original meaning while making it natural for narration
• Adjusts pacing and structure to fit your selected time duration"
                      required
                    />
                    <div className="form-text">
                      <i className="fas fa-lightbulb me-1"></i>
                      Input any script and we'll transform it into engaging, human-like narration
                    </div>
                  </div>
                )}

                {/* Mode 2: Generate New Script */}
                {mode === 'generate' && (
                  <>
                    <div className="row">
                      <div className="col-md-8 mb-3">
                        <label htmlFor="topic" className="form-label">
                          <i className="fas fa-lightbulb me-1 text-success"></i>
                          Topic *
                        </label>
                        <input 
                          type="text" 
                          className="form-control" 
                          name="topic"
                          value={formData.topic}
                          onChange={handleInputChange}
                          placeholder="e.g., Mysterious disappearance of Flight MH370"
                          required
                        />
                      </div>
                      <div className="col-md-4 mb-3">
                        <label htmlFor="genre" className="form-label">
                          <i className="fas fa-theater-masks me-1 text-success"></i>
                          Genre *
                        </label>
                        <select 
                          className="form-select" 
                          name="genre"
                          value={formData.genre}
                          onChange={handleInputChange}
                        >
                          <option value="mysterious">Mysterious</option>
                          <option value="thriller">Thriller</option>
                          <option value="investigative">Investigative</option>
                          <option value="motivational">Motivational</option>
                          <option value="inspirational">Inspirational</option>
                          <option value="dramatic">Dramatic</option>
                          <option value="educational">Educational</option>
                          <option value="informative">Informative</option>
                        </select>
                      </div>
                    </div>

                    <div className="mb-3">
                      <label htmlFor="description" className="form-label">
                        <i className="fas fa-align-left me-1 text-success"></i>
                        Additional Description (Optional)
                      </label>
                      <textarea 
                        className="form-control" 
                        name="description" 
                        rows="3"
                        value={formData.description}
                        onChange={handleInputChange}
                        placeholder="Add any specific details, context, or requirements for your script..."
                      />
                    </div>
                  </>
                )}

                {/* Duration Selection */}
                <div className="mb-4">
                  <label htmlFor="duration_seconds" className="form-label">
                    <i className="fas fa-clock me-1 text-primary"></i>
                    Target Duration *
                  </label>
                  <select 
                    className="form-select" 
                    name="duration_seconds"
                    value={formData.duration_seconds}
                    onChange={handleInputChange}
                  >
                    <optgroup label="Short Format">
                      <option value="30">30 seconds (Quick Hook)</option>
                      <option value="45">45 seconds (Standard Short)</option>
                      <option value="60">60 seconds (Detailed Short)</option>
                    </optgroup>
                    <optgroup label="Medium Format">
                      <option value="120">2 minutes (Brief Story)</option>
                      <option value="180">3 minutes (Standard Story)</option>
                    </optgroup>
                    <optgroup label="Long Format">
                      <option value="300">5 minutes (Full Story)</option>
                      <option value="600">10 minutes (Detailed Analysis)</option>
                    </optgroup>
                  </select>
                </div>

                {/* API Key (Optional) */}
                <div className="mb-4">
                  <label htmlFor="api_key" className="form-label">
                    <i className="fas fa-key me-1 text-secondary"></i>
                    Custom Gemini API Key (Optional)
                  </label>
                  <input 
                    type="password" 
                    className="form-control" 
                    name="api_key"
                    value={formData.api_key}
                    onChange={handleInputChange}
                    placeholder="Enter your API key for priority access"
                  />
                  <div className="form-text">
                    <i className="fas fa-info-circle me-1"></i>
                    Using your own API key provides faster processing and unlimited usage
                  </div>
                </div>

                {error && (
                  <div className="alert alert-danger" role="alert">
                    <i className="fas fa-exclamation-triangle me-2"></i>
                    {error}
                  </div>
                )}

                <div className="d-grid">
                  <button type="submit" className="btn btn-primary btn-lg" disabled={loading}>
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        {mode === 'humanize' ? 'Humanizing Script...' : 'Generating Script...'}
                      </>
                    ) : (
                      <>
                        <i className={`fas ${mode === 'humanize' ? 'fa-magic' : 'fa-pen-nib'} me-2`}></i>
                        {mode === 'humanize' ? 'Humanize Script' : 'Generate Script'}
                      </>
                    )}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

        {/* Results Section */}
        <div className="col-lg-6">
          {result && (
            <div className="card shadow-lg border-0">
              <div className="card-header bg-success text-white border-0">
                <h5 className="card-title mb-0">
                  <i className="fas fa-check-circle me-2"></i>
                  Generated Script
                </h5>
              </div>
              <div className="card-body">
                <div className="accordion" id="resultAccordion">
                  {/* Title */}
                  <div className="accordion-item">
                    <h2 className="accordion-header">
                      <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#titleCollapse">
                        <i className="fas fa-heading me-2"></i>
                        Title
                      </button>
                    </h2>
                    <div id="titleCollapse" className="accordion-collapse collapse show" data-bs-parent="#resultAccordion">
                      <div className="accordion-body">
                        <div className="d-flex justify-content-between align-items-start">
                          <p className="mb-0 fw-bold">{result.title}</p>
                          <button className="btn btn-outline-secondary btn-sm" onClick={() => copyToClipboard(result.title)}>
                            <i className="fas fa-copy"></i>
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Script */}
                  <div className="accordion-item">
                    <h2 className="accordion-header">
                      <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#scriptCollapse">
                        <i className="fas fa-file-text me-2"></i>
                        Voice Over Script
                      </button>
                    </h2>
                    <div id="scriptCollapse" className="accordion-collapse collapse" data-bs-parent="#resultAccordion">
                      <div className="accordion-body">
                        <div className="d-flex justify-content-between align-items-start mb-2">
                          <button className="btn btn-outline-secondary btn-sm" onClick={() => copyToClipboard(result.vo_script)}>
                            <i className="fas fa-copy me-1"></i> Copy Script
                          </button>
                        </div>
                        <div className="border p-3 rounded bg-light">
                          <pre className="mb-0" style={{whiteSpace: 'pre-wrap'}}>{result.vo_script}</pre>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* On-screen Text */}
                  {result.on_screen_text && (
                    <div className="accordion-item">
                      <h2 className="accordion-header">
                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#textCollapse">
                          <i className="fas fa-tv me-2"></i>
                          On-Screen Text
                        </button>
                      </h2>
                      <div id="textCollapse" className="accordion-collapse collapse" data-bs-parent="#resultAccordion">
                        <div className="accordion-body">
                          <div className="d-flex justify-content-between align-items-start mb-2">
                            <button className="btn btn-outline-secondary btn-sm" onClick={() => copyToClipboard(result.on_screen_text.join('\n'))}>
                              <i className="fas fa-copy me-1"></i> Copy Text
                            </button>
                          </div>
                          <ul className="list-unstyled">
                            {result.on_screen_text.map((text, index) => (
                              <li key={index} className="mb-2">
                                <span className="badge bg-primary me-2">{index + 1}</span>
                                {text}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Description */}
                  <div className="accordion-item">
                    <h2 className="accordion-header">
                      <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#descCollapse">
                        <i className="fas fa-align-left me-2"></i>
                        Description
                      </button>
                    </h2>
                    <div id="descCollapse" className="accordion-collapse collapse" data-bs-parent="#resultAccordion">
                      <div className="accordion-body">
                        <div className="d-flex justify-content-between align-items-start mb-2">
                          <button className="btn btn-outline-secondary btn-sm" onClick={() => copyToClipboard(result.description)}>
                            <i className="fas fa-copy me-1"></i> Copy Description
                          </button>
                        </div>
                        <div className="border p-3 rounded bg-light">
                          <pre className="mb-0" style={{whiteSpace: 'pre-wrap'}}>{result.description}</pre>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Hashtags */}
                  {result.hashtags && (
                    <div className="accordion-item">
                      <h2 className="accordion-header">
                        <button className="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#hashtagCollapse">
                          <i className="fas fa-hashtag me-2"></i>
                          Hashtags ({result.hashtags.length})
                        </button>
                      </h2>
                      <div id="hashtagCollapse" className="accordion-collapse collapse" data-bs-parent="#resultAccordion">
                        <div className="accordion-body">
                          <div className="d-flex justify-content-between align-items-start mb-2">
                            <button className="btn btn-outline-secondary btn-sm" onClick={() => copyToClipboard(result.hashtags.join(' '))}>
                              <i className="fas fa-copy me-1"></i> Copy All
                            </button>
                          </div>
                          <div>
                            {result.hashtags.map((tag, index) => (
                              <span key={index} className="badge bg-info me-1 mb-1">{tag}</span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
