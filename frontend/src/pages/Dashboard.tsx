import React from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
} from '@mui/material';
import {
  Business as BusinessIcon,
  People as PeopleIcon,
  CalendarMonth as CalendarIcon,
} from '@mui/icons-material';

const Dashboard: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        ダッシュボード
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <Box>
              <Typography color="text.secondary" gutterBottom>
                部署数
              </Typography>
              <Typography variant="h4">-</Typography>
            </Box>
            <BusinessIcon sx={{ fontSize: 60, color: 'primary.main' }} />
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <Box>
              <Typography color="text.secondary" gutterBottom>
                従業員数
              </Typography>
              <Typography variant="h4">-</Typography>
            </Box>
            <PeopleIcon sx={{ fontSize: 60, color: 'primary.main' }} />
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <Box>
              <Typography color="text.secondary" gutterBottom>
                今月のシフト
              </Typography>
              <Typography variant="h4">-</Typography>
            </Box>
            <CalendarIcon sx={{ fontSize: 60, color: 'primary.main' }} />
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              クイックスタート
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              1. 部署管理から部署を登録してください
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              2. 従業員管理から従業員を登録してください
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              3. シフトカレンダーからシフトを自動生成できます
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
