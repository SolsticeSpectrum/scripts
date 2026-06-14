#include <ntddk.h>

void sus()
{
    int* p = NULL;
    *p = 0;
}

ntstatus DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath)
{
    UNREFERENCED_PARAMETER(RegistryPath);
    DriverObject->DriverUnload = NULL;
    sus();
    return STATUS_SUCCESS;
}
