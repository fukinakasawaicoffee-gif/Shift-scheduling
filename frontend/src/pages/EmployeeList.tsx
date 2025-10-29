import React from 'react';
import { Container, Typography, Paper } from '@mui/material';

const EmployeeList: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom>
        従業員管理
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="body1">
          従業員管理機能（実装予定）
        </Typography>
      </Paper>
    </Container>
  );
};

export default EmployeeList;
