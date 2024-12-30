import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useState, useEffect } from 'react';
import { Box, Checkbox } from '@mui/joy';
import { ListItem } from '@mui/joy';
import { List } from '@mui/joy';

const USE_FOLLOWER_COUNT = 'USE_FOLLOWER_COUNT';
const ONLY_DIFF = 'ONLY_DIFF';

const Graph = () => {
    const [timelineD, setTimelineD] = useState<
        Record<string, Array<{
            id: string;
            account_deleted: boolean;
            newly_followed: boolean;
            unfollowed: boolean;
        }>>
    >({});
    const [followersCache, setFollowersCache] = useState<Record<string, number>>({});
    const [flags, setFlags] = useState<Array<string>>([]);

    const toTimeline = (data: Record<string, Array<{
        id: string;
        account_deleted: boolean;
        newly_followed: boolean;
        unfollowed: boolean;
    }>>) => {
        let sum = 0
        const isUseFollowerCount = flags.includes(USE_FOLLOWER_COUNT);
        const timeline = Object.entries(data).map(([dateRange, followers]) => {
            const [_, end] = dateRange.split('_').filter(x => x.match(/^\d+$/));
            const date = new Date(parseInt(end) * 1000).toISOString().split('T')[0];
            const netChange = followers.reduce((acc, curr) => {
                const id: string = curr.id;
                const followerCount = (isUseFollowerCount ? followersCache[id] : 1) ?? 0;
                return acc + (curr.newly_followed ? followerCount : 0) - (curr.unfollowed ? followerCount : 0) - (curr.account_deleted ? followerCount : 0);
            }, 0);

            if (flags.includes(ONLY_DIFF)) {
                sum = netChange;
            } else {
                sum += netChange;
            }

            return {
                date,
                followers: sum
            };
        });
        return timeline;
    };

    // Process data for the char
    useEffect(() => {
        fetch("/diff_cache.json")
            .then((response) => response.json())
            .then((data) => {
                setTimelineD(data);
            });
        fetch("/followers_cache.json")
            .then((response) => response.json())
            .then((data) => {
                setFollowersCache(data);
            });
    }, []);
    return (
        <Box>

            <List
                orientation="horizontal"
                wrap
                sx={{ '--List-gap': '8px', '--ListItem-radius': '20px', mt: 1 }}
            >
                {[
                    USE_FOLLOWER_COUNT,
                    ONLY_DIFF,
                ].map((item) => (
                    <ListItem key={item}>
                        <Checkbox
                            overlay
                            variant="soft"
                            label={item}
                            checked={flags.includes(item)}
                            onChange={(event) => {
                                setFlags(prev =>
                                    event.target.checked
                                        ? [...prev, item]
                                        : prev.filter(f => f !== item)
                                )
                            }}
                        />
                    </ListItem>
                ))}
            </List>
            <ResponsiveContainer width="100%" height={500}>
                <LineChart
                    data={toTimeline(timelineD)}
                    margin={{ top: 20, right: 40, bottom: 40, left: 40 }}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line
                        type="monotone"
                        dataKey="followers"
                        name="Net Follower Change"
                        stroke="#8884d8"
                        fill="#8884d8"
                    />
                </LineChart>
            </ResponsiveContainer>
        </Box>
    );
};

export default Graph;
