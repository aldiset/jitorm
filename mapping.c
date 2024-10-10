#include <Python.h>

static PyObject* map_to_instance(PyObject* self, PyObject* args) {
    PyObject *cls, *data, *dict, *fields, *field;
    PyObject *value;
    Py_ssize_t i, data_len;

    // Parse arguments, expecting a class and a tuple of data
    if (!PyArg_ParseTuple(args, "OO", &cls, &data)) {
        return NULL;
    }

    // Check if the second argument is a tuple
    if (!PyTuple_Check(data)) {
        PyErr_SetString(PyExc_TypeError, "Expected a tuple, got something else");
        return NULL;
    }

    // Get the '_fields' attribute from the class, assuming it's a list
    fields = PyObject_GetAttrString(cls, "_fields");
    if (!PyList_Check(fields)) {  // _fields should be a list, not a dict
        PyErr_SetString(PyExc_TypeError, "Class _fields attribute is not a list");
        return NULL;
    }

    // Check that the size of the data matches the size of the fields list
    data_len = PyTuple_Size(data);
    if (data_len != PyList_Size(fields)) {
        PyErr_SetString(PyExc_ValueError, "Data length does not match the number of fields");
        return NULL;
    }

    // Create a new dictionary to hold the field-value mappings
    dict = PyDict_New();
    for (i = 0; i < data_len; i++) {
        field = PyList_GetItem(fields, i);  // Get field name
        value = PyTuple_GetItem(data, i);   // Get corresponding value

        // Set the field-value pair in the dictionary
        PyDict_SetItem(dict, field, value);
    }

    // Create an instance of the class by passing the dictionary to the class constructor
    PyObject *instance = PyObject_Call(cls, PyTuple_Pack(1, dict), NULL);
    Py_DECREF(dict);  // Decrease reference to the dictionary

    return instance;
}

static PyMethodDef JITMethods[] = {
    {"map_to_instance", map_to_instance, METH_VARARGS, "Create an instance from a tuple"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef jitmodule = {
    PyModuleDef_HEAD_INIT,
    "jit_wrapper",
    NULL,
    -1,
    JITMethods
};

PyMODINIT_FUNC PyInit_jit_wrapper(void) {
    return PyModule_Create(&jitmodule);
}
