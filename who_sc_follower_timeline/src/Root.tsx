import { Box, Button, Divider, ToggleButtonGroup, Typography } from "@mui/joy";
import App from "./App";
import { useState } from "react";
import Graph from "./Graph";

enum View {
    ListHistory = "list_history",
    Graph = "graph",
}

const Root = () => {
    const [view, setView] = useState<View>(View.ListHistory);
    return <Box>
        <h2>@jumang4423 sc analysis</h2>
        <Box mb={2}>
            <Box>
                scraped from soundcloud, then analyzed with python.
                <br />
                understandable that soundcloud doesn't provide api for this but...
            </Box>
        </Box>
        <Box>
            <ToggleButtonGroup
                size={"sm"}
                value={view}
                onChange={(_, newValue) => {
                    setView(newValue as View);
                }}
            >
                <Button value={View.ListHistory}>List History</Button>
                <Button value={View.Graph}>Graph</Button>
            </ToggleButtonGroup>

        </Box>
        <Box mt={2}>
            <Divider />
        </Box>
        {view === View.ListHistory && <App />}
        {view === View.Graph && <Graph />}
    </Box >
}

export default Root;
