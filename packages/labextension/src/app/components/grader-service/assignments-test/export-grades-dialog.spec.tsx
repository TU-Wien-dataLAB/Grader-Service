import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ExportGradesDialog } from '../assignments/export-grades-dialog';
import { useMutationStatus } from '../../../../widget';

jest.mock('../../../../widget', () => ({
  useMutationStatus: jest.fn()
}));

// Mock services
jest.mock('../../../../services/lectures.service', () => ({
  exportGrades: jest.fn()
}));

jest.mock('../../../../services/local-file.service', () => ({
  lectureBasePath: '/lectures/',
  openInNewTab: jest.fn()
}));

// const mockedExportGrades = exportGrades as jest.MockedFunction<
//   typeof exportGrades
// >;
//
// const mockedOpenFile = openInNewTab as jest.MockedFunction<typeof openInNewTab>;
//
// const mockedGoToPath = openInFileBrowser as jest.MockedFunction<
//   typeof openInFileBrowser
// >;

const mockSetStatus = jest.fn();

beforeEach(() => {
  jest.clearAllMocks();
  (useMutationStatus as jest.Mock).mockReturnValue({
    setStatus: mockSetStatus
  });
});

const lecture = {
  id: 'lecture-123',
  code: 'CS101',
  name: 'Introduction to Programming'
} as any;

const renderDialog = (isOpen = true, setIsOpen = jest.fn()) => {
  return {
    setIsOpen,
    ...render(
      <ExportGradesDialog
        lecture={lecture}
        isOpen={isOpen}
        setIsOpen={setIsOpen}
      />
    )
  };
};

describe('ExportGradesDialog', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the dialog when isOpen is true', () => {
    renderDialog();

    expect(
      screen.getByRole('heading', {
        name: 'Export assignments'
      })
    ).toBeInTheDocument();

    expect(screen.getByRole('button', { name: 'Export' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Cancel' })).toBeInTheDocument();
  });

  it('does not render the dialog when isOpen is false', () => {
    renderDialog(false);

    expect(
      screen.queryByRole('heading', {
        name: 'Export assignments'
      })
    ).not.toBeInTheDocument();
  });

  it('uses csv and best as the default selections', () => {
    renderDialog();

    expect(screen.getByText('CSV')).toBeInTheDocument();
    expect(screen.getByText('Best submissions')).toBeInTheDocument();
  });
  // it('opens format select', async () => {
  //   const user = userEvent.setup();
  //   renderDialog();
  //
  //   const select = screen.getByRole('combobox', { name: 'Format' });
  //
  //   await user.click(select);
  //
  //   await waitFor(() =>
  //     expect(select).toHaveAttribute('aria-expanded', 'true')
  //   );
  //
  //   const jsonOption = await screen.findByRole('option', { name: 'JSON' });
  //   const csvOption = await screen.findByRole('option', { name: 'CSV' });
  //   expect(jsonOption).toBeInTheDocument();
  //   expect(csvOption).toBeInTheDocument();
  // });

  // it('exports best submissions as CSV by default', async () => {
  //   mockedExportGrades.mockResolvedValue(undefined);
  //   mockedOpenFile.mockResolvedValue(undefined);
  //   mockedGoToPath.mockResolvedValue(undefined);
  //
  //   const setIsOpen = jest.fn();
  //
  //   renderDialog(true, setIsOpen);
  //
  //   fireEvent.click(screen.getByRole('button', { name: 'Export' }));
  //
  //   await waitFor(() => {
  //     expect(mockedExportGrades).toHaveBeenCalledWith(
  //       'lecture-123',
  //       'best',
  //       'csv'
  //     );
  //   });
  //   expect(mockedOpenFile).toHaveBeenCalledWith(
  //     '/lectures/CS101/Introduction to Programming_best_submissions.csv'
  //   );
  //   expect(mockedGoToPath).toHaveBeenCalledWith('/lectures/CS101');
  //   expect(setIsOpen).toHaveBeenCalledWith(false);
  // });
  // it('closes the dialog when Cancel is clicked', () => {
  //   const setIsOpen = jest.fn();
  //   renderDialog(true, setIsOpen);
  //   fireEvent.click(screen.getByRole('button', { name: 'Cancel' }));
  //   expect(setIsOpen).toHaveBeenCalledWith(false, expect.anything());
  // });

  // it('closes the dialog even when export fails', async () => {
  //   const error = new Error('Export failed');
  //
  //   mockedExportGrades.mockRejectedValue(error);
  //
  //   const consoleErrorSpy = jest
  //     .spyOn(console, 'error')
  //     .mockImplementation(() => {});
  //
  //   const setIsOpen = jest.fn();
  //
  //   renderDialog(true, setIsOpen);
  //
  //   fireEvent.click(screen.getByRole('button', { name: 'Export' }));
  //
  //   await waitFor(() => {
  //     expect(mockedExportGrades).toHaveBeenCalledWith(
  //       'lecture-123',
  //       'best',
  //       'csv'
  //     );
  //   });
  //
  //   expect(consoleErrorSpy).toHaveBeenCalledWith(
  //     'Error exporting grades:',
  //     error
  //   );
  //   expect(setIsOpen).toHaveBeenCalledWith(false);
  //   consoleErrorSpy.mockRestore();
  // });

  // it('does not open the file or navigate when exportGrades fails', async () => {
  //   mockedExportGrades.mockRejectedValue(new Error('Export failed'));
  //   jest.spyOn(console, 'error').mockImplementation(() => {});
  //   const setIsOpen = jest.fn();
  //   renderDialog(true, setIsOpen);
  //   fireEvent.click(screen.getByRole('button', { name: 'Export' }));
  //   await waitFor(() => {
  //     expect(mockedExportGrades).toHaveBeenCalled();
  //   });
  //   expect(mockedOpenFile).not.toHaveBeenCalled();
  //   expect(mockedGoToPath).not.toHaveBeenCalled();
  //   expect(setIsOpen).toHaveBeenCalledWith(false);
  // });
});
