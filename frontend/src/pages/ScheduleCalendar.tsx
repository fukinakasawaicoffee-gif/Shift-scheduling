import React from 'react';
import { Container, Typography, Paper } from '@mui/material';

const ScheduleCalendar: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        シフトカレンダー
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="body1">
          シフトカレンダー機能（実装予定）
        </Typography>
      </Paper>
    </Container>
  );
};

export default ScheduleCalendar;
