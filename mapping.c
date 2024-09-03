#include <Python.h>

static PyObject* map_to_instance(PyObject* self, PyObject* args) {
    PyObject *cls, *data, *dict, *key, *value;
    PyObject *fields, *field;
    Py_ssize_t i, data_len;

    if (!PyArg_ParseTuple(args, "OO", &cls, &data)) {
        return NULL;
    }

    if (!PyTuple_Check(data)) {
        PyErr_SetString(PyExc_TypeError, "Expected a tuple, got something else");
        return NULL;
    }

    fields = PyObject_GetAttrString(cls, "_fields");
    if (!PyDict_Check(fields)) {
        PyErr_SetString(PyExc_TypeError, "Class _fields attribute is not a dictionary");
        return NULL;
    }

    data_len = PyTuple_Size(data);
    if (data_len != PyDict_Size(fields)) {
        PyErr_SetString(PyExc_ValueError, "Data length does not match the number of fields");
        return NULL;
    }

    dict = PyDict_New();
    for (i = 0; i < data_len; i++) {
        field = PyList_GetItem(fields, i);
        value = PyTuple_GetItem(data, i);
        PyDict_SetItem(dict, field, value);
    }

    PyObject *instance = PyObject_Call(cls, PyTuple_Pack(1, dict), NULL);
    Py_DECREF(dict);

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
