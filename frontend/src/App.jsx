import { useEffect, useMemo, useState } from "react";

import {
  Activity,
  Wind,
  MapPin,
  RefreshCw,
  Search,
  AlertTriangle,
  TrendingUp,
} from "lucide-react";

import "./App.css";

const API_URL = "http://127.0.0.1:8000/api/v1";

function getAQIStatus(aqi) {
  if (aqi <= 50) return { label: "Good", color: "#16a34a" };
  if (aqi <= 100) return { label: "Moderate", color: "#ca8a04" };

  if (aqi <= 150) {
    return {
      label: "Unhealthy for Sensitive Groups",
      color: "#ea580c",
    };
  }

  if (aqi <= 200) return { label: "Unhealthy", color: "#dc2626" };
  if (aqi <= 300) return { label: "Very Unhealthy", color: "#9333ea" };

  return { label: "Hazardous", color: "#7f1d1d" };
}

function App() {
  const [readings, setReadings] = useState([]);
  const [totalCities, setTotalCities] = useState(0);
  const [dataSource, setDataSource] = useState("Open-Meteo");
  const [dataKind, setDataKind] = useState("modelled");
  const [lastUpdated, setLastUpdated] = useState("");

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  // Fetch all 103 city readings from one endpoint
  async function loadDashboard() {
    try {
      setError("");

      const response = await fetch(`${API_URL}/aqi/latest`);

      if (!response.ok) {
        throw new Error("Unable to fetch AQI data from backend.");
      }

      const result = await response.json();

      const data = Array.isArray(result.readings)
        ? result.readings
        : [];

      setReadings(data);
      setTotalCities(result.total_cities ?? data.length);
      setDataSource(result.data_source || "Open-Meteo");
      setDataKind(result.data_kind || "modelled");
      setLastUpdated(new Date().toLocaleString("en-IN"));

    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  // Refresh backend AQI data
  async function handleRefresh() {
    try {
      setRefreshing(true);
      setError("");

      const response = await fetch(`${API_URL}/aqi/refresh`, {
        method: "POST",
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.detail || "Unable to refresh AQI data.");
      }

      await loadDashboard();

    } catch (err) {
      setError(err.message || "Refresh failed.");
    } finally {
      setRefreshing(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  // Sort all readings by US AQI, highest first
  const rankings = useMemo(() => {
    return [...readings].sort(
      (a, b) => Number(b.us_aqi ?? -1) - Number(a.us_aqi ?? -1)
    );
  }, [readings]);

  // Search all cities by city or state
  const filteredCities = useMemo(() => {
    const query = search.trim().toLowerCase();

    return rankings.filter((city) => {
      return (
        `${city.city || ""} ${city.state || ""}`
          .toLowerCase()
          .includes(query)
      );
    });
  }, [rankings, search]);

  // Calculate average AQI using all available readings
  const validReadings = readings.filter(
    (city) => city.us_aqi !== null && city.us_aqi !== undefined
  );

  const averageAQI = validReadings.length
    ? Math.round(
        validReadings.reduce(
          (sum, city) => sum + Number(city.us_aqi),
          0
        ) / validReadings.length
      )
    : "--";

  const worstCity = rankings[0];

  const bestCity = rankings.length
    ? rankings[rankings.length - 1]
    : null;

  return (
    <div className="dashboard">

      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <Wind size={25} />
          </div>

          <div>
            <h2>LIVE AQI</h2>
            <span>INDIA MONITOR</span>
          </div>
        </div>

        <div className="sidebar-label">MAIN MENU</div>

        <nav>
          <a className="nav-item active" href="#overview">
            <Activity size={18} />
            Overview
          </a>

          <a className="nav-item" href="#cities">
            <MapPin size={18} />
            Cities
          </a>

          <a className="nav-item" href="#rankings">
            <TrendingUp size={18} />
            AQI Rankings
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="live-indicator">
            <span />
            DATA AVAILABLE
          </div>

          <p>Air quality intelligence across India.</p>
        </div>
      </aside>

      <main className="main-content" id="overview">

        <header className="topbar">
          <div>
            <p className="eyebrow">INDIA / AIR QUALITY</p>

            <h1>Air Quality Dashboard</h1>

            <p className="subtitle">
              Monitor air quality across {totalCities || 0} Indian city entries.
            </p>
          </div>

          <button
            className="refresh-button"
            onClick={handleRefresh}
            disabled={refreshing || loading}
          >
            <RefreshCw
              size={16}
              className={refreshing ? "spin" : ""}
            />

            {refreshing ? "Refreshing..." : "Refresh Data"}
          </button>
        </header>

        {error && (
          <div className="error-message">
            <AlertTriangle size={18} />
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading">Loading air quality data...</div>
        ) : (
          <>

            <section className="stats-grid">

              <div className="stat-card">
                <div className="stat-heading">
                  <span>Total Cities</span>
                  <MapPin />
                </div>

                <h2>{totalCities}</h2>
                <p>City entries monitored</p>
              </div>

              <div className="stat-card">
                <div className="stat-heading">
                  <span>Average US AQI</span>
                  <Activity />
                </div>

                <h2>{averageAQI}</h2>
                <p>Across available readings</p>
              </div>

              <div className="stat-card">
                <div className="stat-heading">
                  <span>Most Polluted</span>
                  <AlertTriangle />
                </div>

                <h2 className="city-stat">
                  {worstCity?.city || "--"}
                </h2>

                <p>
                  US AQI: {worstCity?.us_aqi ?? "--"}
                </p>
              </div>

              <div className="stat-card">
                <div className="stat-heading">
                  <span>Data Source</span>
                  <Wind />
                </div>

                <h2 className="source-stat">{dataSource}</h2>

                <p>{dataKind} air-quality estimates</p>
              </div>

            </section>

            <section className="section" id="rankings">

              <div className="section-heading">
                <div>
                  <p className="eyebrow">CITY PERFORMANCE</p>
                  <h2>Most Polluted Cities</h2>

                  <p className="section-description">
                    Cities ranked by US AQI, highest to lowest.
                  </p>
                </div>

                <span className="live-badge">
                  {rankings.length} READINGS
                </span>
              </div>

              <div className="table-container">
                <table>
                  <thead>
                    <tr>
                      <th>RANK</th>
                      <th>CITY</th>
                      <th>STATE</th>
                      <th>US AQI</th>
                      <th>PM2.5</th>
                      <th>PM10</th>
                      <th>STATUS</th>
                    </tr>
                  </thead>

                  <tbody>
                    {rankings.map((city, index) => {
                      const aqi = Number(city.us_aqi);
                      const status = getAQIStatus(aqi);

                      return (
                        <tr key={`${city.city}-${city.state}-${index}`}>
                          <td className="rank-number">
                            #{index + 1}
                          </td>

                          <td className="city-name">{city.city}</td>
                          <td>{city.state}</td>

                          <td className="aqi-value">
                            {city.us_aqi ?? "--"}
                          </td>

                          <td>{city.pm2_5 ?? "--"}</td>
                          <td>{city.pm10 ?? "--"}</td>

                          <td>
                            <span
                              className="status"
                              style={{
                                color: status.color,
                                backgroundColor: `${status.color}18`,
                              }}
                            >
                              {status.label}
                            </span>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>

                {rankings.length === 0 && (
                  <p className="empty-state">
                    No AQI readings available.
                  </p>
                )}
              </div>

            </section>

            <section className="section" id="cities">

              <div className="section-heading">
                <div>
                  <p className="eyebrow">EXPLORE LOCATIONS</p>
                  <h2>All Monitored Cities</h2>

                  <p className="section-description">
                    Search and explore every monitored city entry.
                  </p>
                </div>

                <div className="search-box">
                  <Search size={17} />

                  <input
                    type="text"
                    placeholder="Search city or state..."
                    value={search}
                    onChange={(event) => setSearch(event.target.value)}
                  />

                  {search && (
                    <button
                      className="clear-search"
                      onClick={() => setSearch("")}
                      aria-label="Clear search"
                    >
                      ×
                    </button>
                  )}
                </div>
              </div>

              <div className="results-count">
                Showing {filteredCities.length} of {totalCities} cities
              </div>

              <div className="city-grid">
                {filteredCities.map((city, index) => {
                  const aqi = Number(city.us_aqi);
                  const status = getAQIStatus(aqi);

                  return (
                    <div
                      className="city-card"
                      key={`${city.city}-${city.state}-${index}`}
                    >
                      <div className="city-card-icon">
                        <MapPin size={18} />
                      </div>

                      <div className="city-details">
                        <h3>{city.city}</h3>
                        <p>{city.state}</p>
                      </div>

                      <div className="city-aqi">
                        <strong>{city.us_aqi ?? "--"}</strong>
                        <span style={{ color: status.color }}>
                          {status.label}
                        </span>
                      </div>
                    </div>
                  );
                })}

                {filteredCities.length === 0 && (
                  <p className="empty-state">
                    No cities found. Try another search.
                  </p>
                )}
              </div>

            </section>

            <footer>
              <span>LIVE AQI INDIA</span>

              <span>
                {dataKind} estimates · {dataSource}
              </span>

              <span>
                Last loaded: {lastUpdated || "--"}
              </span>
            </footer>

          </>
        )}

      </main>
    </div>
  );
}

export default App;