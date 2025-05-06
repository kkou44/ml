Sub ReadSpecificCSV()

    Dim fileName As String
    Dim currentDir As String
    Dim fullPath As String
    Dim nextSheetIndex As Integer
    Dim newSheet As Worksheet
    Dim fileNameSheet As Worksheet
    Dim currentRow As Integer
    Dim csvWorkbook As Workbook

    currentDir = ThisWorkbook.Path
    If Right(currentDir, 1) <> "/" Then
        currentDir = currentDir & "/"
    End If

    Set fileNameSheet = ThisWorkbook.Sheets("Sheet1") ' オブジェクトは Set を使う
    currentRow = 1
    nextSheetIndex = 1

    Do While fileNameSheet.Cells(currentRow, 1).Value <> ""

        fileName = fileNameSheet.Cells(currentRow, 1).Value
        fullPath = currentDir & fileName

        If Dir(fullPath) <> "" Then
            ' CSVファイルを開く
            Set csvWorkbook = Workbooks.Open(fileName:=fullPath)

            ' アクティブシートをコピー（ThisWorkbook に）
            csvWorkbook.Sheets(1).Copy After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count)

            ' コピーされたシートの名前を設定
            Set newSheet = ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count)
            On Error Resume Next
            newSheet.Name = "Imported" & nextSheetIndex
            On Error GoTo 0

            ' CSVファイルは閉じる（保存しない）
            csvWorkbook.Close SaveChanges:=False

            nextSheetIndex = nextSheetIndex + 1
        Else
            MsgBox "ファイルが見つかりません: " & fullPath, vbExclamation
        End If

        currentRow = currentRow + 1
    Loop

    MsgBox "完了しました", vbInformation

End Sub


Sub CreateScatterChartColored()

    Dim chartSheet As Worksheet
    Dim chartObj As ChartObject
    Dim chart As chart
    Dim i As Integer
    Dim ws As Worksheet
    Dim seriesX As Range, seriesY As Range
    Dim markerStyle As Integer

    On Error Resume Next
    Application.DisplayAlerts = False
    ThisWorkbook.Sheets("ScatterPlot").Delete
    Application.DisplayAlerts = True
    On Error GoTo 0

    Set chartSheet = ThisWorkbook.Sheets.Add
    chartSheet.Name = "ScatterPlot"

    Set chartObj = chartSheet.ChartObjects.Add(Left:=100, Top:=50, Width:=600, Height:=400)
    Set chart = chartObj.chart
    chart.ChartType = xlXYScatter

    For i = 1 To 3
        Set ws = Nothing
        On Error Resume Next
        Set ws = ThisWorkbook.Sheets("Imported" & i)
        On Error GoTo 0

        If ws Is Nothing Then
            MsgBox "シート Imported" & i & " が見つかりません", vbExclamation
            Exit Sub
        End If

        Select Case i
            Case 1: markerStyle = xlMarkerStyleCircle
            Case 2: markerStyle = xlMarkerStyleSquare
            Case 3: markerStyle = xlMarkerStyleDiamond
            Case 4: markerStyle = xlMarkerStyleTriangle
            Case Else: markerStyle = xlMarkerStyleX
        End Select

        ' 青いマーカー（列A-B）
        Set seriesX = ws.Range("A1", ws.Cells(ws.Rows.Count, 1).End(xlUp))
        Set seriesY = ws.Range("B1", ws.Cells(ws.Rows.Count, 2).End(xlUp))
        Call Plot(chart, seriesX, seriesY, markerStyle, "Imported" & i & " - A/B", 0, 112, 192)

        ' 赤いマーカー（列C-D）
        Set seriesX = ws.Range("C1", ws.Cells(ws.Rows.Count, 3).End(xlUp))
        Set seriesY = ws.Range("D1", ws.Cells(ws.Rows.Count, 4).End(xlUp))
        Call Plot(chart, seriesX, seriesY, markerStyle, "Imported" & i & " - C/D", 192, 0, 0)

        Set seriesX = ws.Range("E1", ws.Cells(ws.Rows.Count, 5).End(xlUp))
        Set seriesY = ws.Range("F1", ws.Cells(ws.Rows.Count, 6).End(xlUp))
        Call Plot(chart, seriesX, seriesY, markerStyle, "Imported" & i & " - C/D", 0, 176, 80)
    Next i

    chart.HasTitle = True
    chart.ChartTitle.Text = "Scatter Plot of Imported Data"
    chart.HasLegend = True

    With chart.Axes(xlCategory)
        .MinimumScale = -10
        .MaximumScale = 10
    End With

    With chart.Axes(xlValue)
        .MinimumScale = -10
        .MaximumScale = 10
    End With

    With chart.Axes(xlCategory)
        .HasTitle = True
        .AxisTitle.Text = "X Axis Name"
    End With

    With chart.Axes(xlValue)
        .HasTitle = True
        .AxisTitle.Text = "Y Axis Name"
    End With

    MsgBox "散布図を作成しました。", vbInformation

End Sub

Sub Plot(chart As chart, seriesX As Range, seriesY As Range, markerStyle As Integer, seriesName As String, r As Integer, g As Integer, b As Integer)
    chart.SeriesCollection.NewSeries

    With chart.SeriesCollection(chart.SeriesCollection.Count)
        .XValues = seriesX
        .values = seriesY
        .Name = seriesName
        .markerStyle = markerStyle
        .MarkerForegroundColor = RGB(0, 0, 0)
        .MarkerBackgroundColor = RGB(r, g, b)
    End With
End Sub


