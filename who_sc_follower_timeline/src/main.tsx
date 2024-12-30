import ReactDOM from 'react-dom/client'
import Root from './Root'
import { Box } from '@mui/joy';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <Box sx={{
    fontFamily: 'Iosevka',
    margin: "0 16px",
  }}>
    <link
      rel="stylesheet"
      href="https://cdn.xeiaso.net/static/css/iosevka/family.css"
    />
    <Root />
  </Box>
);
