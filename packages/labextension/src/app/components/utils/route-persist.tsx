import { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router';

const STORAGE_KEY = 'lastRoute';

export default function RoutePersist(): null {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const savedRoute = localStorage.getItem(STORAGE_KEY);
    if (savedRoute && location.pathname === '/') {
      navigate(savedRoute, { replace: true });
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(
      STORAGE_KEY,
      location.pathname + location.search + location.hash
    );
  }, [location]);

  return null;
}
